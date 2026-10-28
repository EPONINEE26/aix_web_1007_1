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

# def login(request):
#     return render(request, 'login,html')

# def step01(request):     
#     BASE_DIR = Path(__file__).resolve().parent.parent
#     ENV_FILE = BASE_DIR / ".env"
#     load_dotenv(ENV_FILE)
#     naver_key = os.getenv('naver_key')
#     print('네이버인증키 : ',naver_key)
#     return render(request, 'step01.html')   

# def step02(request):
#     return render(request, 'step02.html')

# def step03(request):
#     return render(request, 'step03.html')

# def step04(request):
#     return render(request, 'step04.html')

# def emailsend(request):
#     email = request.POST.get('email','')
#     print('이메일주소확인 :', email)
    
#     BASE_DIR = Path(__file__).resolve().parent.parent
#     ENV_FILE = BASE_DIR / ".env"
#     load_dotenv(ENV_FILE)
#     naver_key = os.getenv('naver_key')
#     print('네이버인증키 : ',naver_key)
    
#     chars = string.digits + string.ascii_lowercase
#     e_key = ''.join(random.choice(chars,k=10))
#     print(e_key)
    
#     sendEmail = "tracey212@naver.com"
#     content = f'이메일확인 인증키 : {e_key}'
    
#     msg = MIMEText(content)    
#     msg['From'] = sendEmail 
#     msg['To'] = email               
#     msg['Subject'] = '이메일 TEST3'    
    
#     s = smtplib.SMTP("smtp.naver.com",587) 
#     s.starttls() 
#     s.login(sendEmail,naver_key) 
#     s.sendmail(sendEmail,email,msg.as_string()) 
#     s.close() 
    
#     request.session['session_e_key'] = e_key
#     context = {'e_key':e_key}
#     return JsonResponse(context)

# def ekey(request):
#     email_key = request.POST.get('email_key','')
#     session_e_key = request.session['session_e_key']
#     print(f'데이터 확인 : {email_key},{session_e_key}')
#     if email_key == session_e_key:
#         context = {'temp':1}
#     else:
#         context = {'temp':0}
        
#     return JsonResponse(context)



def login(request):
    return render(request, 'login.html')


def ekey(request):
    # 인증키가져오기
    email_key = request.POST.get('email_key','')

    # 수정 3: 세션에 인증번호가 없어도 KeyError가 발생하지 않도록 get() 사용
    session_e_key = request.session.get('session_e_key','')

    print(f"데이터 확인 : {email_key},{session_e_key}")

    # 수정 4: 입력값과 세션값이 모두 빈 문자열일 때 인증 성공하지 않도록 조건 추가
    if email_key != '' and email_key == session_e_key:
        context = {'temp':1}
    else:
        context = {'temp':0}

    return JsonResponse(context)


def emailsend(request):
    email = request.POST.get('email', '')
    print('이메일주소확인 :', email)

    BASE_DIR = Path(__file__).resolve().parent.parent
    ENV_FILE = BASE_DIR / ".env"
    print('ENV 파일 존재 여부 :', ENV_FILE.exists())

    load_dotenv(ENV_FILE)
    naver_key = os.getenv('naver_key')
    print('비밀번호 로딩 여부 :', bool(naver_key))

    # 수정 5: 이메일이 입력되지 않았으면 SMTP 연결을 시도하지 않고 실패 반환
    if email == '':
        return JsonResponse({'temp':0, 'error':'이메일 주소가 없습니다.'})

    # 수정 6: .env에서 naver_key를 가져오지 못했으면 원인을 반환
    if not naver_key:
        return JsonResponse({'temp':0, 'error':'naver_key를 불러오지 못했습니다.'})

    chars = string.digits + string.ascii_lowercase

    # 수정 7: secrets.choice()를 기존 수업 코드인 random.choices()로 복원
    # 이유: 이미 import random이 있으므로 secrets 미정의 오류가 발생하지 않음
    e_key = ''.join(random.choices(chars, k=10))

    print('생성된 이메일 인증번호 :', e_key)

    # 기존에 실제 사용하던 네이버 발신 이메일 주소를 입력해야 함
    sendEmail = 'tracey212@naver.com'

    content = f'이메일확인 인증키 : {e_key}'

    # 수정 8: 한글 이메일 본문이 깨지지 않도록 UTF-8 지정
    msg = MIMEText(content, _charset='utf-8')

    msg['From'] = sendEmail
    msg['To'] = email
    msg['Subject'] = '이메일 TEST2'

    try:
        s = smtplib.SMTP("smtp.naver.com", 587)
        print('SMTP 서버 연결 성공')

        s.starttls()
        print('TLS 연결 성공')

        print('SMTP 로그인 시도')
        s.login(sendEmail, naver_key)
        print('SMTP 로그인 성공')

        s.sendmail(sendEmail, email, msg.as_string())
        print('이메일 발송 성공')
        s.close()

    except smtplib.SMTPAuthenticationError as e:
        print('SMTP 로그인 실패')
        print('오류번호 :', e.smtp_code)
        print('오류내용 :', e.smtp_error)

        # 수정 9: SMTP 로그인 실패를 JSON으로 반환
        # status=500을 지정하지 않아 AJAX에서 응답 내용을 확인하기 쉽게 처리
        return JsonResponse({
            'temp':0,
            'error':'SMTP 로그인 실패'
        })

    # 수정 10: SMTP 인증 실패 외의 서버 연결·발송 오류도 확인
    except (smtplib.SMTPException, OSError) as e:
        print('SMTP 연결 또는 발송 실패 :', e)

        return JsonResponse({
            'temp':0,
            'error':'SMTP 연결 또는 발송 실패'
        })

    request.session['session_e_key'] = e_key

    context = {'e_key': e_key}
    return JsonResponse(context)


def step01(request):
    BASE_DIR = Path(__file__).resolve().parent.parent
    ENV_FILE = BASE_DIR / ".env"
    load_dotenv(ENV_FILE)
    naver_key = os.getenv('naver_key')

    # 수정 11: SMTP 비밀번호 자체를 CMD에 출력하지 않고 로딩 여부만 확인
    print('네이버인증키 로딩 여부 : ', bool(naver_key))

    return render(request, 'step01.html')


def step02(request):
    return render(request,'step02.html')


def step03(request):
    return render(request,'step03.html')


def step04(request):
    return render(request,'step04.html')
