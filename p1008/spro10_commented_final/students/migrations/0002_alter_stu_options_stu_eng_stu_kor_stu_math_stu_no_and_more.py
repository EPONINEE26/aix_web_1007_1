# 최초 테이블 생성 뒤 Stu 모델에 추가된 변경 사항을 기록한 마이그레이션.
# models.py를 수정한 뒤 makemigrations가 만든 데이터베이스 변경 설계도.

from django.db import migrations, models


class Migration(migrations.Migration):
    # 0001_initial.py가 먼저 적용되어 students_stu 테이블이 존재해야 함.
    dependencies = [
        ('students', '0001_initial'),
    ]

    # migrate가 순서대로 실행할 데이터베이스 변경 목록.
    operations = [
        migrations.AlterModelOptions(
            # Stu 조회 결과의 기본 정렬 규칙 변경.
            # models.py의 Meta.ordering = ['no', 'id']와 연결.
            name='stu',
            options={'ordering': ['no', 'id']},
        ),

        # 영어 점수 열 추가. 빈 값 대신 0을 기본값으로 저장.
        migrations.AddField(
            model_name='stu',
            name='eng',
            field=models.PositiveIntegerField(default=0, verbose_name='영어'),
        ),

        # 국어 점수 열 추가.
        migrations.AddField(
            model_name='stu',
            name='kor',
            field=models.PositiveIntegerField(default=0, verbose_name='국어'),
        ),

        # 수학 점수 열 추가.
        migrations.AddField(
            model_name='stu',
            name='math',
            field=models.PositiveIntegerField(default=0, verbose_name='수학'),
        ),

        # 엑셀의 번호 열 추가.
        # blank와 null을 허용하지만, 값이 있으면 unique로 중복 방지.
        migrations.AddField(
            model_name='stu',
            name='no',
            field=models.PositiveIntegerField(
                blank=True,
                null=True,
                unique=True,
                verbose_name='번호',
            ),
        ),

        # 엑셀 학교 열을 저장할 문자열 필드 추가.
        migrations.AddField(
            model_name='stu',
            name='school',
            field=models.CharField(
                blank=True,
                max_length=100,
                verbose_name='학교',
            ),
        ),

        # 엑셀 키 열을 저장할 0 이상 정수 필드 추가.
        migrations.AddField(
            model_name='stu',
            name='stature',
            field=models.PositiveIntegerField(
                default=0,
                verbose_name='키',
            ),
        ),

        # 엑셀 SW특기 열을 저장할 문자열 필드 추가.
        migrations.AddField(
            model_name='stu',
            name='sw',
            field=models.CharField(
                blank=True,
                max_length=100,
                verbose_name='SW특기',
            ),
        ),
    ]
