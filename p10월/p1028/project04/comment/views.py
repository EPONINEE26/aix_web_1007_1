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
from comment.models import Comment
from event.models import Event
from member.models import Member

def commlist(request):
    context = {'result':'성공'}
    return JsonResponse(context)

# ajax 댓글쓰기
def commWrite(request):
    eno = request.POST.get('eno')
    # ForeignKey는 객체1개 전체를 입력해야 함.
    e_qs = Event.objects.get(eno=eno)
    m_qs = Member.objects.get(id=request.session['session_id'])
    cpw = request.POST.get('cpw','')
    ccontent = request.POST.get('ccontent')
    # Comment저장 - qs:cno,event,member,cpw,ccontent,cdate
    qs = Comment.objects.create(
        event=e_qs,member=m_qs,cpw=cpw,ccontent=ccontent)
    print(f'확인:{eno},{cpw},{ccontent},{qs.cno},{qs.cdate}')
    # Json타입으로 변경
    qs_1 = list(Comment.objects.filter(cno=qs.cno).values())
    context = {'result':'성공','comment':qs_1}
    return JsonResponse(context)
    

# ajax 댓글쓰기
# def commWrite(request):
#     # [추가] 로그인 안 한 상태면 아래 request.session['session_id'] 에서 KeyError 가 나서 댓글이 등록되지 않음
#     #        -> 먼저 확인해서 'login' 이라는 값을 화면(eview.html)에 돌려줌
#     if 'session_id' not in request.session:
#         return JsonResponse({'result':'login'})
#     eno = request.POST.get('eno')
#     # ForeignKey는 객체1개 전체를 입력해야 함.
#     e_qs = Event.objects.get(eno=eno)
#     m_qs = Member.objects.get(id=request.session['session_id'])
#     cpw = request.POST.get('cpw','')
#     ccontent = request.POST.get('ccontent')
#     # Comment저장 - qs:cno,event,member,cpw,ccontent,cdate
#     qs = Comment.objects.create(
#         event=e_qs,member=m_qs,cpw=cpw,ccontent=ccontent)
#     print(f'확인:{eno},{cpw},{ccontent},{qs.cno},{qs.cdate}')
#     # Json타입으로 변경
#     qs_1 = list(Comment.objects.filter(cno=qs.cno).values())
#     context = {'result':'성공','comment':qs_1}
#     return JsonResponse(context)