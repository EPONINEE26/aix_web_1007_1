"""
학생 엑셀 파일을 관리자용 StudentScore 모델에 넣는 Django 관리 명령.

터미널에서 다음처럼 실행하는 파일:
python manage.py import_students

전체 처리 순서:
1. 프로젝트 루트의 students.xlsx 찾기
2. data 시트 또는 첫 번째 시트 열기
3. 첫 행을 헤더로 읽고 필요한 열이 모두 있는지 확인
4. 각 학생 행을 모델 필드에 맞는 딕셔너리로 변환
5. 번호가 같은 기존 학생은 수정하고, 없는 번호는 새로 생성
"""

# 현재 파일의 위치를 기준으로 students.xlsx의 절대 경로를 만들 때 사용.
from pathlib import Path

# BaseCommand: manage.py 명령의 기본 클래스.
# CommandError: 사용자가 수정할 수 있는 입력 오류를 터미널에 표시할 때 사용.
from django.core.management.base import BaseCommand, CommandError

# 데이터베이스에 StudentScore 테이블이 실제로 있는지 확인할 때 사용.
from django.db import connection

# xlsx 파일을 읽는 함수.
from openpyxl import load_workbook

# 파일이 손상되었거나 xlsx 형식이 아닐 때 발생할 수 있는 오류.
from openpyxl.utils.exceptions import InvalidFileException

# 변환한 값을 저장할 점수 모델.
from stuscore.models import StudentScore


# __file__은 현재 import_students.py의 경로.
# parents[3]은 commands -> management -> students -> 프로젝트 루트 순서로 올라감.
# 결과적으로 manage.py와 같은 위치의 students.xlsx를 가리킴.
EXCEL_FILE = Path(__file__).resolve().parents[3] / 'students.xlsx'


# 엑셀의 한글 제목과 StudentScore 모델의 영어 필드를 연결.
# 열의 실제 순서가 바뀌어도 제목을 기준으로 값을 찾을 수 있게 하는 표.
COLUMN_ALIASES = {
    '번호': 'no',
    '이름': 'name',
    '학교': 'school',
    '학년': 'grade',
    '키': 'stature',
    '국어': 'kor',
    '영어': 'eng',
    '수학': 'math',
    'SW특기': 'sw',
}


def _text(value):
    """엑셀 셀을 DB에 넣을 문자열로 정리하는 함수."""

    # openpyxl은 빈 셀을 None으로 반환.
    # 화면과 DB에서 사용할 빈 문자열로 통일.
    if value is None:
        return ''

    # 숫자나 날짜도 문자열로 바꾸고 셀 양쪽의 불필요한 공백 제거.
    return str(value).strip()


def _number(value, header):
    """엑셀 셀을 정수로 바꾸고 숫자가 아니면 어느 열인지 알려주는 함수."""

    try:
        # 엑셀의 90, 90.0, '90' 같은 값을 정수 90으로 통일.
        return int(float(value))

    except (TypeError, ValueError) as exc:
        # value가 None이거나 글자일 때 어느 헤더에서 오류가 발생했는지 표시.
        # from exc는 원래 오류 원인도 함께 보존.
        raise CommandError(
            f'{header} 열에 숫자가 아닌 값이 있음: {value!r}'
        ) from exc


def read_excel_rows():
    """
    엑셀 전체를 읽어 StudentScore.objects에 전달할 딕셔너리 목록 반환.

    반환 예시:
    {
        'no': 1,
        'name': '홍길동',
        'school': '가나고',
        ...
    }
    """

    # 파일이 없을 때 load_workbook까지 실행하면 이해하기 어려운 오류가 발생하므로
    # 먼저 파일 존재 여부를 검사하고 명확한 CommandError를 발생.
    if not EXCEL_FILE.exists():
        raise CommandError(
            f'{EXCEL_FILE} 파일이 없음. '
            'manage.py와 같은 위치에 students.xlsx를 배치'
        )

    try:
        # read_only=True: 수정 없이 읽기만 하므로 큰 엑셀 파일의 메모리 사용량 감소.
        # data_only=True: 수식 코드가 아니라 엑셀에 저장된 계산 결과를 읽음.
        workbook = load_workbook(
            EXCEL_FILE,
            read_only=True,
            data_only=True,
        )
    except (InvalidFileException, OSError, ValueError) as exc:
        # 파일 형식 오류, 운영체제 파일 접근 오류, 잘못된 값 오류를 사용자 메시지로 변경.
        raise CommandError(
            'students.xlsx를 열 수 없음. 올바른 xlsx 파일인지 확인'
        ) from exc

    try:
        # data라는 이름의 시트를 우선 사용.
        # 해당 시트가 없으면 엑셀의 첫 번째 시트를 사용.
        if 'data' in workbook.sheetnames:
            worksheet = workbook['data']
        else:
            worksheet = workbook.worksheets[0]

        # values_only=True이므로 셀 객체가 아니라 셀 값만 행별 튜플로 반환.
        rows = worksheet.iter_rows(values_only=True)

        try:
            # 첫 번째 행을 헤더로 분리.
            # 이후 rows에는 두 번째 행부터 학생 데이터만 남음.
            raw_headers = next(rows)
        except StopIteration as exc:
            # next()할 행이 없다는 것은 헤더조차 없는 빈 시트라는 뜻.
            raise CommandError('엑셀 시트에 헤더 행이 없음') from exc

        # None, 숫자, 공백이 섞인 헤더를 비교 가능한 문자열로 정리.
        headers = [_text(value) for value in raw_headers]

        # enumerate(): 헤더 목록의 번호와 값을 동시에 꺼냄.
        # {'번호': 0, '이름': 1}처럼 헤더명과 실제 열 위치를 연결.
        indexes = {
            header: index
            for index, header in enumerate(headers)
            if header
        }

        # COLUMN_ALIASES의 모든 한글 헤더가 엑셀에 있는지 검사.
        missing = [
            header
            for header in COLUMN_ALIASES
            if header not in indexes
        ]

        if missing:
            # 누락된 헤더를 한 번에 보여줘 엑셀 수정 위치를 알 수 있게 함.
            raise CommandError(
                '엑셀 헤더가 누락됨: ' + ', '.join(missing)
            )

        # 변환이 끝난 학생 딕셔너리를 차례로 담을 목록.
        result = []

        # 헤더 다음의 모든 행을 한 학생씩 처리.
        for raw_row in rows:
            # 값이 하나도 없는 행은 학생 데이터가 아니므로 건너뜀.
            if not any(
                value is not None and str(value).strip()
                for value in raw_row
            ):
                continue

            # 현재 엑셀 행 하나를 모델 저장용 딕셔너리로 변환.
            values = {}

            # 엑셀 한글 헤더를 기준으로 열 위치를 찾고 모델 필드에 저장.
            for excel_header, model_field in COLUMN_ALIASES.items():
                # 예: excel_header='국어'이면 indexes['국어']가 국어 열 번호.
                index = indexes[excel_header]

                # 행의 실제 셀 수가 부족한 비정상 행은 빈 값으로 보완.
                if index < len(raw_row):
                    value = raw_row[index]
                else:
                    value = ''

                # 모델에서 정수로 선언된 필드는 숫자 변환.
                if model_field in {
                    'no',
                    'grade',
                    'stature',
                    'kor',
                    'eng',
                    'math',
                }:
                    values[model_field] = _number(value, excel_header)

                # 이름·학교·SW특기처럼 글자인 필드는 문자열 정리.
                else:
                    values[model_field] = _text(value)

            # 한 학생 변환 결과를 전체 결과 목록에 추가.
            result.append(values)

        return result

    finally:
        # 변환 중 오류가 발생해도 엑셀 파일 핸들을 닫아 파일 잠금 방지.
        workbook.close()


class Command(BaseCommand):
    """python manage.py import_students 실행 시 Django가 호출하는 명령 클래스."""

    # python manage.py help에 표시되는 설명.
    help = 'students.xlsx 데이터를 관리자용 StudentScore 모델로 가져옴'

    def handle(self, *args, **options):
        # 엑셀을 읽고 모델 필드명으로 바꾼 학생 목록.
        students = read_excel_rows()

        created_count = 0
        updated_count = 0

        # 학생 딕셔너리를 한 명씩 DB에 반영.
        for values in students:
            # StudentScore 테이블에서 번호가 같은 행 검색.
            # 있으면 defaults의 값으로 수정, 없으면 새 행 생성.
            # _는 수정된 객체를 사용하지 않겠다는 의미로 반환값 하나를 버림.
            # created는 새로 생성되었으면 True, 기존 수정이면 False.
            _, created = StudentScore.objects.update_or_create(
                no=values['no'],
                defaults=values,
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        # self.stdout: Django 관리 명령의 터미널 출력 객체.
        # style.SUCCESS: 성공 결과를 터미널에서 구분되는 형식으로 출력.
        self.stdout.write(
            self.style.SUCCESS(
                f'완료: 신규 {created_count}명, '
                f'갱신 {updated_count}명, '
                f'전체 {len(students)}명'
            )
        )
