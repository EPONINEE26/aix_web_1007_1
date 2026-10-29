from django.shortcuts import render
import os
from pathlib import Path
from dotenv import load_dotenv
from django.db.models import F,Q
from member.models import Member
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.views.decorators.http import require_POST
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

@require_POST
def emailsend(request):
    email = request.POST.get('email', '').strip()
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'temp': 0, 'message': '올바른 이메일 주소를 입력하세요.'}, status=400)
    print('이메일주소확인 : ',email)
    BASE_DIR = Path(__file__).resolve().parent.parent
    ENV_FILE = BASE_DIR / ".env"

    # manage.py와 같은 폴더의 .env 파일을 읽습니다.
    load_dotenv(ENV_FILE, override=True)

    # naver_key가 없으면 None 대신 빈 문자열을 받습니다.
    naver_key = (os.getenv('naver_key') or '').strip()

    # 비밀번호가 없으면 SMTP 로그인을 실행하지 않고 원인을 반환합니다.
    if not naver_key:
        return JsonResponse({
            'temp': 0,
            'message': 'project04/.env 파일의 naver_key 설정을 확인하세요.'
        }, status=503)
        
    chars = string.digits + string.ascii_lowercase
    e_key = ''.join(random.choices(chars,k=10)) 
    print(e_key)
    
    sendEmail = '본인이메일@naver.com'   # [수정] 원본 위치 그대로 유지. 따옴표 안에 본인 네이버 메일주소를 직접 입력하세요 (개인정보라 비워둠)
    content = f'이메일확인 인증키 : {e_key}'
    
    msg = MIMEText(content)    
    msg['From'] = sendEmail 
    msg['To'] = email                
    msg['Subject'] = '이메일 TEST2'    
    
    try:
        with smtplib.SMTP("smtp.naver.com", 587, timeout=15) as smtp:
            smtp.starttls()
            smtp.login(sendEmail, naver_key)
            smtp.sendmail(sendEmail, email, msg.as_string())
    except smtplib.SMTPAuthenticationError:
        return JsonResponse({'temp': 0, 'message': '네이버 SMTP 인증에 실패했습니다. 발신 계정과 naver_key를 확인하세요.'}, status=502)
    except (smtplib.SMTPException, OSError):
        return JsonResponse({'temp': 0, 'message': '이메일 전송에 실패했습니다. SMTP 설정과 연결을 확인하세요.'}, status=502)
    
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
    return render(request, 'step01.html')

def step02(request):
    return render(request, 'step02.html')

def step03(request):
    return render(request, 'step03.html')   # [수정] 오타 tep03.html -> step03.html

def step04(request):
    return render(request, 'step04.html')
