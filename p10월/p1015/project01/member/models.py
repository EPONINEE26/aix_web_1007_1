from django.db import models

class Member(models.Model):
    
    # primary Key : 중복불가, null 불가
    # foreign Key (외래키): 다른 클래스에서 primaryKey로 사용된 것을 사용할 때 
    id = models.CharField(max_length=30,primary_key=True)
    pw = models.CharField(max_length=100)
    name = models.CharField(max_length=60)
    nickname = models.CharField(max_length=60)
    tel = models.CharField(max_length=20) 
    gender = models.CharField(max_length=6)
    hobby = models.CharField(max_length=100)
    mdate = models.DateTimeField(auto_now=True,blank=True) # 빈 공백 가능하게 한다는 의미

    def __str__(self):
        return f'{self.id},{self.pw},{self.name},{self.nickname},{self.tel},{self.gender},{self.hobby},{self.mdate}'