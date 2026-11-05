from django.urls import path, include
from.import views

app_name='screen'
urlpatterns = [
    path('chart', views.chart, 'chart'),
    path('chart_data', views.chart_data, name='chart_data'),
    
    path('map', views.map, name='map'),
]
