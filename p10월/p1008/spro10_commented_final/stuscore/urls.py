from django.urls import path

from . import views

.
app_name = 'stuscore'
urlpatterns = [
    path('score_write/', views.score_write, name='score_write'),
    path('score_swrite/', views.score_write, name='score_swrite'),
]
