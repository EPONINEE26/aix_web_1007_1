
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('step01/', views.step01, name='step01'),
    path('step02/', views.step02, name='step02'),
    path('step03/', views.step03, name='step03'),
    path('step04/', views.step04, name='step04'),
    
    path('emailsend/', views.emailsend, name='emailsend'),
    path('ekey/', views.ekey, name='ekey'),


]

