from django.urls import path,include
from . import views

app_name='board'
urlpatterns = [
    # 차트그래프 
    path('chart/', views.chart, name='chart'),
    # 차트그래프 데이터
    path('chart_data/', views.chart_data, name='chart_data'),
        
    path('blist/', views.blist, name='blist'),
    path('bwrite/', views.bwrite, name='bwrite'),
    path('bview/<int:bno>/', views.bview, name='bview'),
    path('bupdate/<int:bno>/', views.bupdate, name='bupdate'),
    path('bdelete/<int:bno>/', views.bdelete, name='bdelete'),
    path('breply/<int:bno>/', views.breply, name='breply'),
]

