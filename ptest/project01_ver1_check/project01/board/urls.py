from django.urls import path
from . import views

app_name = 'board'
urlpatterns = [
    path('blist/', views.blist, name='blist'),
    path('bwrite/', views.bwrite, name='bwrite'),
    path('bview/<int:bno>/', views.bview, name='bview'),
    path('bupdate/<int:bno>/', views.bupdate, name='bupdate'),
    path('bdelete/<int:bno>/', views.bdelete, name='bdelete'),
    path('breply/<int:bno>/', views.breply, name='breply'),

    path('commWrite/<int:bno>/', views.commWrite, name='commWrite'),
    path('commUpdate/<int:bno>/<int:cno>/', views.commUpdate, name='commUpdate'),
    path('commDelete/<int:bno>/<int:cno>/', views.commDelete, name='commDelete'),
]