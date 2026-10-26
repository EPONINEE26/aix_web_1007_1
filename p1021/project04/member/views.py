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
            # 로그인 전에 저장해 둔 답변 작성 페이지 주소를 가져온다.
            # pop()은 주소를 가져오면서 세션에 저장된 'reply_next' 항목을 삭제한다.
            # None은 저장된 주소가 없을 때 오류 대신 반환하는 기본값이다.
            reply_next = request.session.pop('reply_next', None) 
            
            # 가져온 주소가 존재하고, 그 주소가 답변 작성 페이지로 시작하는지 확인한다.
            # 두 조건이 모두 참일 때만 아래 코드를 실행한다.            
            if reply_next and reply_next.startswith('/board/breply/'): # 앞에서 가져온 주소가 실제로 답변 작성 화면의 주소인지 확인하는 조건문
                
                # 수정: 답변 작성 화면으로 이동하기 전 원본 로그인 성공 안내 표시
                # 로그인 성공 후 답변 작성 페이지에서 사용할 표시용 값을 세션에 저장한다.
                # True는 로그인 성공 안내를 표시할 수 있도록 전달하는 값이다.
                request.session['reply_login_success'] = True
                
                # 저장해 둔 답변 작성 페이지 주소로 이동한다.
                # return은 이동 응답을 반환하고 현재 함수를 종료한다.
                return redirect(reply_next)
            context={'temp':1}
        else:
            context={'temp':0}
        print(f'데이터확인 : {id},{pw},{context},{qs}')
        return render(request,'login.html',context)


