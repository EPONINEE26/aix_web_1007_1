from django.urls import path,include
from . import views

app_name='member'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    path('membership1/', views.membership1, name='membership1'),
    path('membership2/', views.membership2, name='membership2'),
    path('membership3/', views.membership3, name='membership3'),
]
