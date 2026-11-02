# Django가 students/models.py의 최초 모델 상태를 기록한 마이그레이션 파일.
# 이 파일은 코드를 실행해 화면을 만드는 파일이 아니라,
# python manage.py migrate 실행 시 데이터베이스 구조를 만드는 변경 기록.

# migrations: 데이터베이스 변경 작업을 표현하는 모듈.
# models: CharField, IntegerField 같은 필드 종류를 기록할 때 사용.
from django.db import migrations, models


# 하나의 마이그레이션 파일을 Django가 읽을 수 있는 형식으로 정의.
class Migration(migrations.Migration):
    # students 앱에서 처음 만들어진 테이블 구조라는 표시.
    initial = True

    # 이 파일보다 먼저 적용해야 하는 마이그레이션이 없음.
    dependencies = []

    # migrate 명령이 실제 데이터베이스에 실행할 변경 목록.
    operations = [
        migrations.CreateModel(
            # models.py의 Stu 클래스를 바탕으로 students_stu 테이블 생성.
            name='Stu',
            fields=[
                # Django가 모든 모델에 자동으로 추가하는 기본 키.
                # primary_key=True라서 각 학생 행을 구분하는 고유 번호가 됨.
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID',
                )),

                # 아래 항목들이 실제 테이블 열로 생성.
                # max_length와 default는 models.py의 필드 설정이 그대로 기록된 것.
                ('name', models.CharField(max_length=100)),
                ('major', models.CharField(max_length=100)),
                ('age', models.IntegerField(default=0)),
                ('grade', models.IntegerField(default=0)),
                ('gender', models.CharField(max_length=30)),
            ],
        ),
    ]
