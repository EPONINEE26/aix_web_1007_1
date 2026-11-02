# URL 패턴을 만드는 Django 함수.
from django.urls import path

# 현재 앱의 views.py를 views라는 이름으로 가져옴.
from . import views


app_name = 'students'
urlpatterns = [
    path('swrite/', views.swrite, name='swrite'),
    path('slist/', views.slist, name='slist'),
]
