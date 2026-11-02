
from django.urls import path, include
from.import views # students 내 view를 찾아감. 같은 폴더 내에는 .을 입력

app_name='students'
urlpatterns = [
    path('swrite/', views.swrite, name='swrite'),
    path('slist/', views.slist, name='slist'),
]