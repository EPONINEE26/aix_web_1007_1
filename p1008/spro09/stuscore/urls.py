from django.urls import path,include
from . import views

app_name='stuscore'
urlpatterns = [
    # 기존 학생성적 입력 URL 유지
    path('score_write/', views.score_write, name='score_write'),

    # 메인 페이지에서 사용하는 URL도 연결
    path('score_swrite/', views.score_write, name='score_swrite'),
]
