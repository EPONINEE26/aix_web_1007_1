from django.shortcuts import render
import os
import re
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
import re


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
    BASE_DIR = Path(__file__).resolve().parent.parent
    ENV_FILE = BASE_DIR / ".env"

    # manage.py와 같은 폴더의 .env 파일을 읽습니다.
    load_dotenv(ENV_FILE, override=True)

    # naver_key가 없으면 None 대신 빈 문자열을 받습니다.
    naver_key = (os.getenv('naver_key') or '').strip()
    print('사용한 설정 파일:', ENV_FILE)
    print('설정 파일 존재:', ENV_FILE.is_file())
    print('SMTP 비밀번호 읽힘:', bool(naver_key))


    # 비밀번호가 없으면 SMTP 로그인을 실행하지 않고 원인을 반환합니다.
    if not naver_key:
        return JsonResponse({
            'temp': 0,
            'message': 'project04/.env 파일의 naver_key 설정을 확인하세요.'
        }, status=503)
        
    chars = string.digits + string.ascii_lowercase
    e_key = ''.join(random.choices(chars,k=10)) 
    
    sendEmail = 'tracey212@naver.com'   # [수정] 원본 위치 그대로 유지. 따옴표 안에 본인 네이버 메일주소를 직접 입력하세요 (개인정보라 비워둠)
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
            
    except smtplib.SMTPAuthenticationError as exc:
            reason = exc.smtp_error
            if isinstance(reason, bytes):
                reason = reason.decode('utf-8', errors='replace')
            reason = str(reason).replace(naver_key, '[비밀번호 숨김]').replace(sendEmail, '[발신 주소 숨김]')
            reason = re.sub(r'[\w.+-]+@[\w.-]+', '[이메일 숨김]', reason)[:500]
            return JsonResponse({
                'temp': 0,
                'message': f'네이버 SMTP 인증이 거부되었습니다. (SMTP {exc.smtp_code}) 사유: {reason}'
            }, status=502)
        
    request.session['session_e_key'] = e_key
    context = {'temp': 1, 'message': '인증키를 이메일로 전송했습니다.'}
    return JsonResponse(context)
  
@require_POST
def ekey(request):
    email_key = request.POST.get('email_key', '').strip()
    session_e_key = request.session.get('session_e_key')
    if not session_e_key:
        return JsonResponse({'temp': 0, 'message': '먼저 이메일로 인증키를 전송하세요.'})
    if not email_key:
        return JsonResponse({'temp': 0, 'message': '인증키를 입력하세요.'})
    if email_key == session_e_key:
        context = {'temp': 1, 'message': '이메일 인증에 성공했습니다.'}
    else:
        context = {'temp': 0, 'message': '인증키가 일치하지 않습니다.'}
    return JsonResponse(context)

def step01(request):
    return render(request, 'step01.html')

def step02(request):
    return render(request, 'step02.html')

def step03(request):
    return render(request, 'step03.html')   # [수정] 오타 tep03.html -> step03.html

def step04(request):
    return render(request, 'step04.html')
