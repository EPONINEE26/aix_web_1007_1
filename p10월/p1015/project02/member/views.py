from django.shortcuts import render
from member.models import Member

def logout(request):
    request.session.clear() 
    # del request.session['session_nickname'] 
    context = {'temp':2}   
    return render(request, 'login.html', context)


def login(request):
    if request.method == 'GET':
        idsave = request.COOKIE.get('cookie_id') 
        
        return render(request, 'login.html')
    elif request.method == 'POST':
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        idsave = request.POST.get('idsave','') # idsave,없을때 빈공백처리
        # 회원확인2
        qs = Member.objects.filter(id=id,pw=pw).first() # qs, None
        if qs:
            # 섹션추가
            request.session['session_id'] = qs.id
            request.session['session_nickname'] = qs.nickname
            context = {'temp':1}
        else:
            context = {'temp':0}

    print(f'로그인정보 : {id},{pw},{idsave} / 회원확인 : {context}')
    response = render(request,'login.html', context)
    if idsave !="":
        response.set_cookie('cookie_id', 'chk', max_age=60*60*24*365) # 60초 60분 24시간 365일 
    else: 
        response.delete_cookie('cookie_id')
    return response
        
        
        
    # try:
    #     qs = Member.objects.get(id=id,pw=pw) # , : and의 의미 # db에 회원 존재 확인
    #     # session 추가 
    #     request.session['session_id'] = qs.id
    #     request.session['session_nickname'] = qs.nickname
    #     context = {'temp':1}
    # except Member.DoesNotExist:
    #     context = {'temp':0}    
    
    # qs = Member.objects.filter(id=id,pw=pw).first() 
    # if qs:    
    #     request.session['session_id'] = qs.id
    #     request.session['session_nickname'] = qs.nickname
    #     context = {'temp':1}
    # else:
    #     context = {'temp':0} 
    # print(f'로그인정보 : {id},{pw} / 회원확인 : {context}')
    # return render(request, 'login.html', context) 
        

    
    
    
def step01(request):
    return render(request, 'step01.html')

def step02(request):
    return render(request, 'step02.html')

def step03(request):
    return render(request, 'step03.html')

def step04(request):
    return render(request, 'step04.html')