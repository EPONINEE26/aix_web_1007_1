
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from openpyxl import load_workbook

from students.models import ExcelStudent


class Command(BaseCommand):
    # 터미널에서 실행할 명령 이름
    help = 'students.xlsx의 학생 정보를 데이터베이스에 가져옵니다.'

    def handle(self, *args, **options):

        # manage.py가 있는 spro08 폴더에서 엑셀 파일을 찾음
        excel_path = Path(settings.BASE_DIR) / 'students.xlsx'

        # 파일이 없으면 경로를 확인할 수 있도록 오류를 표시
        if not excel_path.exists():
            raise CommandError(
                f'엑셀 파일을 찾을 수 없습니다: {excel_path}'
            )

        # data 시트의 첫 번째 행을 열 제목으로 사용
        workbook = load_workbook(
            filename=excel_path,
            read_only=True,
            data_only=True
        )

        # 첨부된 엑셀 파일의 시트 이름은 data
        if 'data' not in workbook.sheetnames:
            workbook.close()
            raise CommandError(
                '엑셀 파일에 data 시트가 없습니다.'
            )

        sheet = workbook['data']

        # 첫 번째 행에서 열 제목을 읽고 앞뒤 공백을 제거
        headers = [
            str(cell.value).strip() if cell.value is not None else ''
            for cell in sheet[1]
        ]

        # 코드가 참조하는 필수 열이 모두 있는지 확인
        required_columns = [
            '번호', '이름', '학교', '학년', '키',
            '국어', '영어', '수학', 'SW특기'
        ]

        missing_columns = [
            column for column in required_columns
            if column not in headers
        ]

        if missing_columns:
            workbook.close()
            raise CommandError(
                '엑셀에서 다음 열을 찾을 수 없습니다: '
                + ', '.join(missing_columns)
            )

        # 각 열 제목이 실제로 몇 번째 위치에 있는지 기록
        # 열의 순서가 바뀌어도 제목으로 데이터를 찾을 수 있음
        column_index = {
            title: headers.index(title)
            for title in required_columns
        }

        imported_count = 0
        skipped_count = 0

        # 두 번째 행부터 마지막 행까지 한 줄씩 읽음            
        for excel_row_number, row in enumerate(
            sheet.iter_rows(min_row=2, values_only=True),
            start=2
        ): 
         # 번호가 비어 있는 행은 데이터 행이 아니므로 건너뜁니다.
            raw_number = row[column_index['번호']]
            if raw_number is None:
                skipped_count += 1
                continue

            try:
                # 엑셀 번호가 정수인지 확인
                number_value = int(raw_number)

                # 필수 숫자 항목은 정수로 변환합니다.
                grade_value = int(row[column_index['학년']])
                height_value = int(row[column_index['키']])
                korean_value = int(row[column_index['국어']])
                english_value = int(row[column_index['영어']])
                math_value = int(row[column_index['수학']])

                # 이름과 학교는 문자열로 정리
                name_value = str(
                    row[column_index['이름']] or ''
                ).strip()

                school_value = str(
                    row[column_index['학교']] or ''
                ).strip()

                # SW특기는 빈 셀이나 None도 빈 문자열로 처리
                sw_value = str(
                    row[column_index['SW특기']] or ''
                ).strip()

                # 번호, 이름, 학교가 없는 행은 저장하지 않음
                if not name_value or not school_value:
                    skipped_count += 1
                    continue

                # 번호가 이미 있으면 해당 학생 정보를 갱신하고,처음 보는 번호라면 새 학생 정보를 생성
                # 따라서 명령을 여러 번 실행해도 번호별 중복 행이 계속 추가되지 않음
                ExcelStudent.objects.update_or_create(
                    number=number_value,
                    defaults={
                        'name': name_value,
                        'school': school_value,
                        'grade': grade_value,
                        'height': height_value,
                        'kor': korean_value,
                        'eng': english_value,
                        'math': math_value,
                        'sw_skill': sw_value,
                    }
                )

                imported_count += 1

            except (TypeError, ValueError) as error:
                # 숫자 칸에 숫자가 아닌 값이 들어 있는 행은 저장하지 않고 어느 행에서 문제가 났는지 표시
                self.stderr.write(
                    f'{sheet.title} 시트의 {excel_row_number}행: '
                    f'데이터 변환 실패 - {error}'
                )   
                skipped_count += 1

        # 엑셀 파일을 다 읽은 후 닫음
        workbook.close()

        # 최종 처리 결과를 터미널에 표시.
        self.stdout.write(
            self.style.SUCCESS(
                f'가져오기 완료: 처리 {imported_count}행, '
                f'건너뜀 {skipped_count}행'
            )
        )