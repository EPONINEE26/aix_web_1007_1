from django.urls import path,include
from . import views

app_name='students'
urlpatterns = [
    path('swrite/', views.swrite, name='swrite'),
    path('slist/', views.slist, name='slist'),
    path('index/', views.index, name='index'),
    
]