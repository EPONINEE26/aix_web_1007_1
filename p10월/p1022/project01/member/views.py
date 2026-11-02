from django.shortcuts import render
import os
from pathlib import Path
from dotenv import load_dotenv
from django.db.models import F,Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import smtplib
from email.mime.text import MIMEText
import random
import string


# 이메일전송
def emailsend(request):
    # 1.email주소
    email = request.POST.get('email','')
    print('이메일주소확인 : ',email)

    # 2. 네이버 비밀번호 가져오기 (.env)
    BASE_DIR = Path(__file__).resolve().parent.parent
    ENV_FILE = BASE_DIR / ".env"
    load_dotenv(ENV_FILE)
    naver_key = os.getenv('naver_key')
    print('네이버인증키 : ',naver_key)

    # 3. 인증키난수생성
    # chars = ['0','1','2','3','4','5','6','7','8','9','a','z']
    #       0-9문자열 + a-z까지 문자열
    chars = string.digits + string.ascii_lowercase
    # 중복가능:choices, 중복불가:sample / 리스트 -> 문자열
    e_key = ''.join(random.choices(chars,k=10))
    print(e_key)

    # 4. 이메일내용 - 글자로 이메일발송
    sendEmail = 'tracey212@naver.com'
    # content = f'이메일확인 인증키 : {e_key}'
    text = f'''
        <html>
            <body>
                <h2>[ 이메일확인 인증키 ]</h2>
                <p>{e_key}</p>
            </body>
        </html>
    '''

    # 5. 정보그룹핑
    msg = MIMEText(text, 'html') # content : 글자만 입력 가능
    # msg = MIMEText(content) # content : 글자만 입력 가능 
    
    msg['From'] = sendEmail # 보내는사람
    msg['To'] = email                # 받는사람
    # msg['Subject'] = '이메일 TEST'    # 제목
    msg['Subject'] = '이메일 TEST2'
    
    
    # 6. 그룹핑 정보전송
    s = smtplib.SMTP("smtp.naver.com",587) #SMTP 서버
    s.starttls() # 메일서버접근
    s.login(sendEmail,naver_key) # 메일서버로그인
    s.sendmail(sendEmail,email,msg.as_string()) # 메일발송
    s.close() # 메일닫기

    # context = {'temp':1}
    request.session['session_e_key'] = e_key
    context = {'temp':e_key} # 이런식으로는 하지 않는 방식 
    return JsonResponse(context)


def ekey(request):
    # 인증키가져오기
    email_key = request.POST.get('email_key','')
    session_e_key = request.session['session_e_key']
    print(f"데이터 확인 : {email_key},{session_e_key}")
    if email_key == session_e_key:
        context = {'temp':1}
    else:
        context = {'temp':0}

    return JsonResponse(context)

# 회원가입1
def step01(request):
    # 디렉토리 위치
    BASE_DIR = Path(__file__).resolve().parent.parent
    ENV_FILE = BASE_DIR / ".env"
    load_dotenv(ENV_FILE)
    naver_key = os.getenv('naver_key')
    print('네이버인증키 : ',naver_key)
    return render(request, 'step01.html')










# def emailsend(request):
#     # email 주소
#     email = request.POST.get('email','') 
#     print('이메일주소확인:','email')  
    
#     # 디렉토리 위치, 네이버비밀번호 가져오기(.env)
#     BASE_DIR = Path(__file__).resolve().parent.parent
#     ENV_FILE = BASE_DIR/".env"
#     load_dotenv(ENV_FILE)
#     naver_key = os.getenv('naver_key')
#     print('네이버인증키 : ',naver_key) 
    
#     # 인증키 난수생성 
#     # chars = ['0','1','2','3','4','5','6','7','8','9','a','b','c']
#     # 0-9까지 문자열 + a~z까지 문자열 리스트로 넘겨줌
#     chars = string.digits + string.ascii_lowercase
#     # e_key = ''.join(random.sample(chars,k=10)) # 리스트를 문자열로 변환해야함
#     e_key = ''.join(random.choice(chars,k=10)) # 중복가능: choice, 중복불가능 : sample
#     print(e_key) 
    
#     # 이메일 발송 - 글자로 email 발송

#     sendEmail = 'tracey212@naver.com'
#     content = f"이메일확인 인증키 : {e_key}"
    
#     # 정보내용그룹핑
#     msg = MIMEText(content)
#     msg['From'] = "sendEmail" # 보내는 사람 
#     msg['To'] = email   # 받는  사람 
#     msg['Subject'] = '이메일 TEST'  # 제목 
    
#     # 그룹핑 정보 전송 
#     s = smtplib.SMTP("smtp.naver.com",587) # SMTP 서버
#     s.starttls() # 메일서버접근    
#     s.login("sendEmail",naver_key) # 메일서버로그인
#     s.sendmail("sendEmail",email,msg.as_string()) # 메일발송
#     s.close()
    
    
    
#     # 이메일 발송 - html형태로 email 발송
    
    
    
    
#     context = {'temp':1}   
#     return JsonResponse(context)



# def step01(request):
#     # 디렉토리 위치 
#     BASE_DIR = Path(__file__).resolve().parent.parent
#     ENV_FILE = BASE_DIR/".env"
#     load_dotenv(ENV_FILE)
#     naver_key = os.getenv('naver_key')
#     print('네이버인증키 : ',naver_key)
    
#     return render(request, 'step01.html')