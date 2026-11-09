from django.db import models
from member.models import Member

class Board(models.Model):
    bno = models.AutoField(primary_key=True)
    id = models.CharField(max_length=30)  
    btitle = models.CharField(max_length=1000)
    bcontent = models.TextField()    # 대용량Text

    bgroup = models.IntegerField(default=0)
    bstep = models.IntegerField(default=0)
    bindent = models.IntegerField(default=0)
    bhit = models.IntegerField(default=1)
    bdate = models.DateTimeField(auto_now=True,blank=True)
    bfile = models.ImageField(blank=True,upload_to='board') 

    def __str__(self):
        return f'{self.bno},{self.btitle},{self.bcontent},{self.bdate}'
    
class Comment(models.Model):
    cno = models.AutoField(primary_key=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)
    display_name = models.CharField(max_length=60, blank=True, default="")
    is_example = models.BooleanField(default=False)
    ccontent = models.TextField()
    cdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.cno)
    