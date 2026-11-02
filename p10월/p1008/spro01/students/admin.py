from django.contrib import admin
from students.models import Stu

admin.site.register(Stu) # 어드민 계정에서 확인 가능한 기능 # primary : 유일 키, 중복 X / foreignkey 


