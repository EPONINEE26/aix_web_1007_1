# from django.urls import path, include
# from.import views

# app_name='member'
# urlpatterns = [
#     path('login/', views.login, name='login'),
#     path('logout/', views.logout, name='logout'),
#     path('step01/', views.step01, name='step01'),
        
#     # path('step02', views.step02, name='step02'),
#     # path('step03', views.step03, name='step03'),
#     # path('step04', views.step04, name='step04'),
    
#     # 이메일전송
#     path('emailsend/', views.emailsend, name='emailsend'),
#     # 이메일전송후 인증키확인
#     path('ekey/', views.ekey, name='ekey'),
    
# ]

#===============================================================


from django.shortcuts import render
import os
from pathlib import Path
from dotenv import load_dotenv
from django.db.models import F,Q
from member.models import Member
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import smtplib                             
from email.mime.text import MIMEText
import random
import string


def login(request):
    if request.method=="GET":
        return render(request,'login.html')
    elif request.method=="POST":
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        qs = Member.objects.filter(id=id,pw=pw)
        if qs :
            qs = qs[0]
            request.session['session_id']=qs.id
            request.session['session_nickname']=qs.nickname
            temp = 1
        else:
            temp = 0
        context = {'temp':temp}
        return render(request,'login.html',context)

def logout(request):
    request.session.clear()
    context = {'temp':2}
    return render(request,'login.html',context)

def emailsend(request):
    email = request.POST.get('email','')
    print('이메일주소확인 : ',email)
    
    BASE_DIR = Path(__file__).resolve().parent.parent
    ENV_FILE = BASE_DIR / ".env"
    load_dotenv(ENV_FILE, override=True)   # [수정] override=True 추가 : PC 환경변수에 예전 naver_key 가 남아있으면 .env 의 새 키보다 우선 사용되어 535 오류가 반복되므로, .env 값을 우선 사용하게 함
    naver_key = os.getenv('naver_key')
    print('네이버인증키 : ',naver_key)
    
    chars = string.digits + string.ascii_lowercase
    e_key = ''.join(random.choices(chars,k=10)) 
    print(e_key)
    
    sendEmail = 'tracey212@naver.com'   
    content = f'이메일확인 인증키 : {e_key}'
    
    msg = MIMEText(content)    
    msg['From'] = sendEmail 
    msg['To'] = email                
    msg['Subject'] = '이메일 TEST2'    
    
    s = smtplib.SMTP("smtp.naver.com",587) 
    s.starttls() 
    s.login(sendEmail,naver_key) 
    s.sendmail(sendEmail,email,msg.as_string()) 
    s.close()  
    
    request.session['session_e_key'] = e_key
    context = {'e_key':e_key}
    return JsonResponse(context)
  
def ekey(request):
    email_key = request.POST.get('email_key','')
    session_e_key = request.session['session_e_key']
    print(f"데이터 확인 : {email_key},{session_e_key}")
    if email_key == session_e_key:
        context = {'temp':1}
    else:
        context = {'temp':0}
    return JsonResponse(context)

def step01(request):
    # 디렉토리 위치
    BASE_DIR = Path(__file__).resolve().parent.parent
    ENV_FILE = BASE_DIR / ".env"
    load_dotenv(ENV_FILE)
    naver_key = os.getenv('naver_key')
    print('네이버인증키 : ',naver_key)
    return render(request, 'step01.html')

def step02(request):
    return render(request, 'step02.html')

def step03(request):
    return render(request, 'step03.html')   

def step04(request):
    return render(request, 'step04.html')

