#!/usr/bin/env python
"""Django 관리 명령의 실행 진입점"""

import os
import sys


def main():
    # Django가 읽을 설정 모듈의 경로를 환경변수에 저장.
    # 이 값으로 spro10/settings.py의 데이터베이스와 앱 설정을 찾음.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spro10.settings')

    try:
        # runserver, migrate, createsuperuser 같은 명령을 처리하는 함수.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Django 패키지가 설치되지 않았거나 현재 Python 환경에서 찾지 못한 경우.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # sys.argv에는 터미널에서 입력한 명령 전체가 들어 있음.
    # 예: ['manage.py', 'runserver']
    # Django가 두 번째 값부터 읽어 실제 관리 작업 실행.
    execute_from_command_line(sys.argv)


# 다른 파일에서 import할 때는 실행하지 않고,
# python manage.py처럼 직접 실행했을 때만 main() 호출.
if __name__ == '__main__':
    main()
