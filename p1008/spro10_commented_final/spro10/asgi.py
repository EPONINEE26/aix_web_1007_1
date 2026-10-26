"""ASGI 방식으로 spro10을 실행하는 진입 파일"""

import os

from django.core.asgi import get_asgi_application

# ASGI 서버가 읽을 Django 설정 모듈 지정.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spro10.settings')

# 외부 ASGI 서버가 HTTP와 비동기 요청을 Django로 전달할 때 사용하는 객체.
application = get_asgi_application()
