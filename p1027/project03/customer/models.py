from django.db import models
from member.models import Member

class Board(models.Model):
    bno = models.AutoField(primary_key=True)
    # id = models.CharField(max_length=30)  # member -> primary_key
    member = models.ForeignKey(Member,on_delete=models.SET_NULL,blank=True,null=True)
    btitle = models.CharField(max_length=1000)
    bcontent = models.TextField()    # 대용량Text
    # 답변달기
    bgroup = models.IntegerField(default=0)
    bstep = models.IntegerField(default=0)
    bindent = models.IntegerField(default=0)
    bhit = models.IntegerField(default=1)
    bdate = models.DateTimeField(auto_now=True,blank=True)
    bfile = models.ImageField(blank=True,upload_to='board') #upload/board폴더를 생성하고 그안에 파일저장

    def __str__(self):
        return f'{self.bno},{self.btitle},{self.bdate}'
