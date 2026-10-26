from django.db import models

class Member(models.Model):
    id = models.CharField(max_length=30,primary_key=True)
    pw = models.CharField(max_length=100)
    name = models.CharField(max_length=60)
    nickname = models.CharField(max_length=60)
    tel = models.CharField(max_length=20) # 031-1203-1111
    gender = models.CharField(max_length=10) # 남자,여자
    hobby = models.CharField(max_length=100) # 남자,여자
    mdate = models.DateTimeField(auto_now=True,blank=True)

    def __str__(self):
        return f'{self.id},{self.pw},{self.name},{self.nickname},{self.tel},{self.gender},{self.hobby},{self.mdate}'