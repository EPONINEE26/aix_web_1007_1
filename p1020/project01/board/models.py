from django.db import models
from member.models import Member

class Board(models.Model):
    # bno = 게시판번호
    # id = 회원아이디
    # btitle : 제목, bcontent : 내용
    # 답변달기 
    # bgroup-답변달기 그룹핑, bstep-그룹순서, bindent-들여쓰기 
    # bhit: 조회수
    # bdate : 게시글 등록일 
    # bfile : 파일첨부   
    
    bno = models.AutoField(primary_key=True)
    # Foreignkey : 다른 테이블에 primary_key등록이 되어 있는 것을 다른 테이블에서 사용할 때
    # Board에 데이터가 등록될 때 Member에서 id값을 확인해서 있는지 체크함     
    # id = models.CharField(max_length=30) 
    member = models.ForeignKey(Member,on_delete=models.SET_NULL,blank=True,null=True)
    # member = models.ForeignKey(Member,on_delete=models.CASCADE,blank=True,null=True) # cascade : 멤버가 삭제가 되면 그 아이디로 쓴 글 모두 삭제 # set_null : 그 아이디로 작성한 글 모두 null 값으로 처리
    # member = models.ForeignKey(Member,on_delete=models.DO_NOTHING,blank=True,null=True) # DO NOTHING을 선정할 경우 null값이나 blank값을 True로 선정해야함. null=:컬럼을 변경하거나 추가할 때 데이터를 어떻게 처리할건지에 대한 문의를 하는 의미 
    btitle = models.CharField(max_length=1000)
    bcontent = models.TextField() # 대용량 text 
    
    # 답변달기
    bgroup = models.IntegerField(default=0)
    bstep = models.IntegerField(default=0)
    bindent = models.IntegerField(default=0)
    bhit = models.IntegerField(default=1)
    bdate = models.DateTimeField(auto_now=True,blank=True)
    bfile = models.ImageField(blank=True,upload_to='board') # 파일첨부할 때 board 폴더에 업로드 


    def __str__(self):
        return f'{self.bno},{self.id},{self.btitle},{self.bcontent},{self.bstep},{self.bindent},{self.bhit},{self.bdate},{self.bfile}'

