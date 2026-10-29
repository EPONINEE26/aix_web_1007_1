from django.urls import path, include
from.import views

app_name='member'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
        
    # GET으로 회원가입 단계별 화면을 표시합니다.
    path('step01/', views.step01, name='step01'),
    path('step02/', views.step02, name='step02'),
    path('step03/', views.step03, name='step03'),
    path('step04/', views.step04, name='step04'),
        
    # path('step02', views.step02, name='step02'),
    # path('step03', views.step03, name='step03'),
    # path('step04', views.step04, name='step04'),
    
    # 이메일전송
    path('emailsend/', views.emailsend, name='emailsend'),
    # 이메일전송후 인증키확인
    path('ekey/', views.ekey, name='ekey'),
    
]

