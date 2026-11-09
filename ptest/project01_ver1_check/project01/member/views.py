from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from .models import Member

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    
    elif request.method == "POST":
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        qs = Member.objects.filter(id=id,pw=pw).first()
        if qs :
            request.session.cycle_key()
            request.session['session_id'] = qs.id
            request.session['session_nickname'] = qs.nickname
            context = {'temp':1}
        else : 
            context = {'temp':0}
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if qs:
                return JsonResponse({'redirect_url': reverse('index')})
            return JsonResponse({'message': '아이디 또는 비밀번호를 확인해 주세요.'}, status=400)
        return render(request, 'login.html', context)

def logout(request):
    request.session.flush()
    context = {'temp':2}
    return render(request, 'login.html', context)


def membership1(request):
    return render(request, 'membership1.html')
