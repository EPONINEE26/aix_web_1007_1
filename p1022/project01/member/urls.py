from django.urls import path,include
from . import views

app_name='member'
urlpatterns = [
    path('step01/', views.step01, name='step01'),
    path('step02/', views.step02, name='step02'),
    
    # 이메일 전송 
    path('emailsend/', views.emailsend, name='emailsend'),
    # 이메일 전송 후 인증키 확인 
    path('ekey/', views.ekey, name='ekey'),
]
