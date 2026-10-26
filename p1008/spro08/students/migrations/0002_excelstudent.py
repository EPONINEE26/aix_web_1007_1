# students 앱의 0001_initial 이후 마이그레이션입니다.
# 기존 Stu 모델 정의를 변경하지 않는 빈 마이그레이션입니다.
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
    ]
