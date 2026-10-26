# 파일 경로를 운영체제에 맞게 조합하기 위한 pathlib의 Path 클래스.
from pathlib import Path

# __file__: 현재 settings.py 파일 경로.
# resolve(): 상대 경로를 절대 경로로 변환.
# parent.parent: spro10 폴더에서 프로젝트 최상위 폴더까지 이동.
# views.py의 students.xlsx 경로와 DATABASES의 db.sqlite3 경로 기준으로 사용.
BASE_DIR = Path(__file__).resolve().parent.parent

# Django가 세션과 보안 기능에 사용하는 비밀 키.
# 개발용 값이며, 실제 배포에서는 외부 환경변수로 관리해야 함.
SECRET_KEY = 'django-insecure-utk#3kmmf27glo(y2v_lnaj+jk^o=fq@cy-zw9js64!w@xe*h#'

# True이면 개발 중 오류 화면과 디버깅 기능 표시.
# 운영 환경에서 켜 두면 내부 정보가 노출될 수 있음.
DEBUG = True

# 요청의 Host 헤더를 검사하는 목록. 개발 단계에서는 비어 있는 상태.
ALLOWED_HOSTS = []

# Django가 시작할 때 함께 활성화할 앱 목록.
# students, home, stuscore가 이 목록에 있어야 모델·템플릿·URL을 앱으로 인식.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'students',
    'home',
    'stuscore',
]

# 요청이 뷰에 도착하기 전후에 공통으로 실행되는 처리 목록.
# CsrfViewMiddleware가 POST 폼의 csrf_token을 검사하므로,
# swrite.html과 score_swrite.html의 {% csrf_token %}과 연결되는 설정.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 가장 먼저 URL을 찾을 프로젝트 URL 파일.
ROOT_URLCONF = 'spro10.urls'

# HTML 템플릿을 어떤 엔진과 경로로 찾을지 지정.
TEMPLATES = [
    {
        # Django 문법 {% if %}, {% for %}, {{ 변수 }}를 처리하는 엔진.
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 앱 밖의 별도 템플릿 폴더는 사용하지 않음.
        'DIRS': [],
        # True이므로 각 앱의 templates 폴더를 자동 검색.
        'APP_DIRS': True,
        'OPTIONS': {
            # 템플릿에서 request, 로그인 사용자, 메시지 등을 사용할 수 있게 하는 함수 목록.
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI 서버가 사용할 Python 경로.
WSGI_APPLICATION = 'spro10.wsgi.application'

# 별도 DB 서버 없이 프로젝트 폴더의 SQLite 파일을 사용.
# BASE_DIR / 'db.sqlite3'은 settings.py 기준 프로젝트 루트의 파일을 가리킴.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 관리자 비밀번호를 검사할 Django 기본 규칙.
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 날짜·시간 표시와 국제화에 사용하는 기본 언어 및 시간대.
LANGUAGE_CODE = 'ko-ko'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

# 정적 파일 URL의 시작 부분.
STATIC_URL = 'static/'

# 현재 프로젝트의 이메일은 외부 발송 대신 개발 콘솔 출력 방식.
MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}
