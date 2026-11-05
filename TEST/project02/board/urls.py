from django.urls import path, include
from.import views 

app_name='board'
urlpatterns = [
    path('bwrite', views.bwrite, name='bwrite'),
    path('blist', views.blist, name='blist'),
    path('bview', views.bview, name='bview'),
    path('bupdate', views.bupdate, name='bupdate'),
    path('bdelete', views.bdelete, name='bdelete'),
    path('breply', views.breply, name='breply'),
    
    path('chart', views.chart, name='chart'),
    path('chart_data', views.chart_data, name='chart_data'),
    
    
]
