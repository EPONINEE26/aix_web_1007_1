
from django.db import models


# 기존 학생 입력 기능에서 사용하던 모델
# 이 모델은 삭제하지 않고 그대로 유지
class Stu(models.Model):
    name = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    grade = models.IntegerField(default=0)
    gender = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name},{self.major},{self.age},{self.grade},{self.gender}'


# 엑셀 파일(students.xlsx)의 학생 정보를 저장하는 모델
# 기존 Stu 모델과 별도의 데이터 테이블을 사용
class ExcelStudent(models.Model):
    # unique=True는 같은 학생 번호가 중복 저장되는 것을 방지
    number = models.PositiveIntegerField(unique=True, verbose_name='번호')
    name = models.CharField(max_length=100, verbose_name='이름')
    school = models.CharField(max_length=100, verbose_name='학교')
    grade = models.PositiveSmallIntegerField(verbose_name='학년')
    # 단위는 원본 데이터 기준으로 표시
    height = models.PositiveSmallIntegerField(verbose_name='키')
    # 각 과목 점수는 0~100점 범위의 정수로 저장합니다.
    korean = models.PositiveSmallIntegerField(verbose_name='국어')
    english = models.PositiveSmallIntegerField(verbose_name='영어')
    math = models.PositiveSmallIntegerField(verbose_name='수학')
    # SW특기는 비어 있을 수 있으므로 blank=True를 지정
    sw_skill = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name='SW특기'
    )

    # 데이터베이스에서 객체를 확인할 때 학생 번호와 이름이 표시
    def __str__(self):
        return f'{self.number}번 - {self.name}'

    # 관리자 화면 등에서 모델을 구분하기 위한 이름
    class Meta:
        verbose_name = '엑셀 학생'
        verbose_name_plural = '엑셀 학생 목록'
        ordering = ['number']