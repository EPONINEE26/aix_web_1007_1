from django.db import models


class Stu(models.Model):
    # 기존 학생 이름 필드
    name = models.CharField(
        max_length=100
    )

    # 기존 학교·전공 필드
    major = models.CharField(
        max_length=100
    )

    # 기존 나이 필드
    age = models.IntegerField(
        default=0
    )

    # 기존 학년 필드
    grade = models.IntegerField(
        default=0
    )

    # 기존 성별 필드
    gender = models.CharField(
        max_length=30
    )

    # 엑셀 번호
    no = models.PositiveIntegerField(
        '번호',
        unique=True,
        null=True,
        blank=True
    )

    # 엑셀 학교
    school = models.CharField(
        '학교',
        max_length=100,
        blank=True
    )

    # 엑셀 키
    stature = models.PositiveIntegerField(
        '키',
        default=0
    )

    # 엑셀 국어 점수
    kor = models.PositiveIntegerField(
        '국어',
        default=0
    )

    # 엑셀 영어 점수
    eng = models.PositiveIntegerField(
        '영어',
        default=0
    )

    # 엑셀 수학 점수
    math = models.PositiveIntegerField(
        '수학',
        default=0
    )

    # 엑셀 SW특기
    sw = models.CharField(
        'SW특기',
        max_length=100,
        blank=True
    )

    class Meta:
        # 번호순 정렬
        ordering = [
            'no',
            'id',
        ]

    def __str__(self):
        # 관리자에서 학생 이름과 학교 표시
        return f'{self.name} ({self.school})'
