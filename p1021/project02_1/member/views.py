from django.shortcuts import render, redirect
from member.models import Member


def logout(request):
    request.session.clear()
    context={'temp':2}
    return render(request,'login.html',context)

def login(request):
    if request.method=="GET":
        return render(request,'login.html')
    
    elif request.method=="POST":
        id=request.POST.get('id')
        pw=request.POST.get('pw')
        qs=Member.objects.filter(id=id,pw=pw).first()
        if qs:
            request.session['session_id']=id
            request.session['session_nickname']=qs.nickname
            # 수정: 답변달기에서 로그인했다면 해당 답변 작성 화면으로 복귀
            reply_next = request.session.pop('reply_next', None)
            if reply_next and reply_next.startswith('/board/breply/'):
                return redirect(reply_next)
            context={'temp':1}
        else:
            context={'temp':0}
        print(f'데이터확인 : {id},{pw},{context},{qs}')
        return render(request,'login.html',context)


