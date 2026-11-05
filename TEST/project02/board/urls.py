from django.urls import path,include
from . import views

app_name='board'
urlpatterns = [
    path('blist', views.blist, name='blist'),
    path('bwrite', views.bwrite, name='bwrite'),
    path('bview', views.bview, name='bview'),
    path('bupdate', views.bupdate, name='bupdate'),
    path('bdelete', views.bdelete, name='bdelete'),
    path('breply', views.breply, name='breply'),
]
