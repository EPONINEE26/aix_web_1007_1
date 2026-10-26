"""WSGI 방식으로 spro10을 실행하는 진입 파일"""

import os

from django.core.wsgi import get_wsgi_application

# WSGI 서버가 Django 설정 위치를 찾을 수 있도록 환경변수 지정.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spro10.settings')

# 외부 WSGI 서버가 이 application 객체를 호출해 웹 요청 전달.
# 일반 개발 명령인 python manage.py runserver에서는 직접 사용할 일이 적음.
application = get_wsgi_application()
