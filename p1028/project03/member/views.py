from django.shortcuts import render
import os
import secrets                                    # [추가] 인증키를 안전하게(예측 불가) 생성하기 위해 random 대신 사용
import string
import smtplib
from pathlib import Path
from email.mime.text import MIMEText
from email.header import Header                   # [추가] 한글 제목 인코딩용
from dotenv import load_dotenv
from django.http import JsonResponse
from django.views.decorators.http import require_POST   # [추가] POST 요청만 허용
from member.models import Member
# [삭제] 사용하지 않는 import(F, Q, csrf_exempt, random) 제거


# # 로그인 - get:로그인페이지, post-로그인확인
# def logout(request):
#     request.session.clear()
#     context = {'temp':2}
#     return render(request,'login.html',context)


# # 로그인 - get:로그인페이지, post-로그인확인
# def login(request):
#     if request.method == 'GET':
#         return render(request,'login.html')
#     elif request.method == 'POST':
#         id = request.POST.get('id')
#         pw = request.POST.get('pw')
#         qs = Member.objects.filter(id=id,pw=pw) # blank -> [0]
#         if qs:
#             qs = qs[0]
#             request.session['session_id'] = qs.id
#             request.session['session_nickname'] = qs.nickname
#             temp = 1
#         else:
#             temp = 0
#         context = {'temp':temp}        
#         return render(request,'login.html',context)



# # 이메일전송후 인증키확인
# def ekey(request):
#     # 인증키가져오기
#     email_key = request.POST.get('email_key','')
#     session_e_key = request.session['session_e_key']
#     print(f"데이터 확인 : {email_key},{session_e_key}")
#     if email_key == session_e_key:
#         context = {'temp':1}
#     else:
#         context = {'temp':0}

#     return JsonResponse(context)


# # 이메일전송
# def emailsend(request):
#     # 1.email주소
#     email = request.POST.get('email','')
#     print('이메일주소확인 : ',email)

#     # 2. 네이버 비밀번호 가져오기 (.env)
#     BASE_DIR = Path(__file__).resolve().parent.parent
#     ENV_FILE = BASE_DIR / ".env"
#     load_dotenv(ENV_FILE)
#     naver_key = os.getenv('naver_key')
#     print('네이버인증키 : ',naver_key)

#     # 3. 인증키난수생성
#     # chars = ['0','1','2','3','4','5','6','7','8','9','a','z']
#     #       0-9문자열 + a-z까지 문자열 
#     chars = string.digits + string.ascii_lowercase
#     # 중복가능:choices, 중복불가:sample / 리스트 -> 문자열
#     e_key = ''.join(random.choices(chars,k=10)) 
#     print(e_key)

#     # 4. 이메일내용 - 글자로 이메일발송
#     sendEmail = 'tracey212@naver.com'
#     content = f'이메일확인 인증키 : {e_key}'
#     text = f'''
#         <html>
#             <body>
#                 <h2>[ 이메일확인 인증키 ]</h2>
#                 <p>{e_key}</p>
#             </body>
#         </html>
#     '''

#     # 5. 정보그룹핑
#     # msg = MIMEText(content)
#     msg = MIMEText(text,'html')
#     msg['From'] = sendEmail # 보내는사람
#     msg['To'] = email                # 받는사람
#     msg['Subject'] = '이메일 TEST2'    # 제목

#     # 6. 그룹핑 정보전송
#     s = smtplib.SMTP("smtp.naver.com",587) #SMTP 서버
#     s.starttls() # 메일서버접근
#     s.login(sendEmail,naver_key) # 메일서버로그인
#     s.sendmail(sendEmail,email,msg.as_string()) # 메일발송
#     s.close() # 메일닫기

#     request.session['session_e_key'] = e_key
#     context = {'e_key':e_key}
#     return JsonResponse(context)

# # 회원가입1
# def step01(request):
#     # 디렉토리 위치
#     BASE_DIR = Path(__file__).resolve().parent.parent
#     ENV_FILE = BASE_DIR / ".env"
#     load_dotenv(ENV_FILE)
#     naver_key = os.getenv('naver_key')
#     print('네이버인증키 : ',naver_key)
#     return render(request, 'step01.html')

# =========================================================

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