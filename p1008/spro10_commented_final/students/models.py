# django.db 안의 models 모듈.
# Django에서 데이터베이스 테이블과 열을 Python 코드로 정의할 때 사용.
from django.db import models


# models.Model을 부모 클래스로 사용하면 Django가 Stu를 데이터베이스 모델로 인식.
# 클래스 안에서 선언한 필드가 데이터베이스 테이블의 열이 되고,
# Stu로 만든 객체 하나가 테이블의 학생 한 명에 해당하는 행이 됨.
class Stu(models.Model):
    # CharField: 글자와 문자열을 저장하는 Django 모델 필드.
    # max_length=100: 이 열에 저장할 수 있는 문자열의 최대 길이.
    # students/templates/swrite.html의 name="name" 값이
    # students/views.py를 거쳐 이 name 열에 저장.
    name = models.CharField(max_length=100)

    # 학과를 글자로 저장하는 열.
    # 입력 폼의 name="major"와 views.py의 major 변수가 이 필드와 연결.
    major = models.CharField(max_length=100)

    # IntegerField: 정수만 저장하는 Django 모델 필드.
    # age 입력값은 HTML에서는 문자열로 들어오지만,
    # Django가 모델 필드 타입에 맞춰 데이터베이스에 정수로 변환.
    # default=0: 값이 전달되지 않았을 때 사용할 기본값.
    age = models.IntegerField(default=0)

    # 학년을 정수로 저장하는 열.
    # 값을 입력하지 않으면 default=0이 적용.
    grade = models.IntegerField(default=0)

    # 성별은 남자·여자처럼 글자로 저장.
    # HTML radio의 value 값이 views.py의 gender를 통해 이 필드로 전달.
    gender = models.CharField(max_length=30)

    # PositiveIntegerField: 0보다 작지 않은 정수만 저장하는 필드.
    # 번호·키·점수처럼 음수가 될 수 없는 값에 적합.
    no = models.PositiveIntegerField(
        # 첫 번째 위치 인자: 관리자 화면과 폼에 표시할 사람이 읽는 필드 이름.
        '번호',

        # unique=True: 데이터베이스 전체에서 같은 번호를 한 번만 허용.
        # 엑셀 재입력 때 번호가 같은 학생을 기존 학생으로 찾는 기준으로 사용 가능.
        unique=True,

        # null=True: 데이터베이스 열 자체에 NULL 저장 허용.
        # 아직 번호가 없는 기존 학생 데이터도 저장할 수 있게 함.
        null=True,

        # blank=True: Django의 폼 입력 검증에서 빈 값 허용.
        # null은 데이터베이스 규칙이고 blank는 입력 검증 규칙이라는 차이가 있음.
        blank=True,
    )

    # CharField의 첫 번째 인자인 '학교'는 관리자 화면의 표시 이름.
    # blank=True이므로 학교를 입력하지 않은 학생도 저장 가능.
    school = models.CharField(
        '학교',
        max_length=100,
        blank=True,
    )

    # 키는 음수가 될 수 없으므로 PositiveIntegerField 사용.
    # 값을 입력하지 않으면 0 저장.
    stature = models.PositiveIntegerField(
        '키',
        default=0,
    )

    # 0점은 허용하지만 음수 점수는 허용하지 않음.
    kor = models.PositiveIntegerField(
        '국어',
        default=0,
    )

    eng = models.PositiveIntegerField(
        '영어',
        default=0,
    )

    math = models.PositiveIntegerField(
        '수학',
        default=0,
    )

    # 특기가 없는 학생도 입력할 수 있도록 blank=True 적용.
    sw = models.CharField(
        'SW특기',
        max_length=100,
        blank=True,
    )

    # Meta: 모델 자체의 데이터 저장 열이 아니라 모델의 기본 동작을 설정하는 내부 클래스.
    class Meta:
        # ordering: objects.all() 같은 목록 조회에 자동으로 적용할 정렬 규칙.
        # 'no'는 번호 오름차순, 'id'는 번호가 같을 때 사용할 보조 정렬 기준.
        # 앞에 '-'가 없으므로 내림차순이 아닌 오름차순.
        # 이 설정 때문에 관리자와 조회 결과가 기본적으로 번호순으로 표시.
        ordering = ['no', 'id']

    # __str__: Python이 객체를 문자열로 바꿀 때 자동으로 호출하는 특수 함수.
    # 관리자 목록, print(student), 디버깅 화면에서 객체 이름을 읽기 쉽게 만드는 용도.
    def __str__(self):
        # self: 현재 문자열로 바꾸려는 Stu 객체 자신.
        # self.name: 현재 학생의 이름 필드 값.
        # self.school: 현재 학생의 학교 필드 값.
        # f-string: 문자열 앞에 f를 붙이고 {} 안에 변수나 표현식을 넣는 문법.
        # 예를 들어 이름이 홍길동이고 학교가 가나고이면
        # 이 함수의 결과는 '홍길동 (가나고)'가 됨.
        return f'{self.name} ({self.school})'
