from django.shortcuts import render
from event.models import Event
from comment.models import Comment
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from member.models import Member

#이벤트리스트 
def event(request):
    qs = Event.objects.all().order_by('-eno')
    context = {'list':qs}
    return render(request, 'event.html',context)

#이벤트 view
def eview(request,eno):
    print('확인 : ',eno)
    qs = Event.objects.filter(eno=eno)[0] # ajax으로 가져오기에 filter로 사용하는 것이 좋고 filter인 경우 리스트로 변환이 가능
    # Foreignkey : event로 저장되어져 있음. 그렇기에 event=qs로 전체를 검색해야함
    qs2 = Comment.objects.filter(event=qs).order_by('-cno')
    qs2_count = qs2.count() # 댓글전체 개수 
    context = {'event':qs,'commlist':qs2,'count':qs2_count}
    return render(request, 'eview.html',context)

# ajax : 좋아요 - 추가,삭제
def likes(request):
    id = request.session['session_id']
    member = Member.objects.get(id=id)
    eno = request.POST.get('eno')   
    event = Event.objects.get(eno=eno) 
    print('확인 :', id,eno)
 
    
    # 해당유저가 좋아요를 클릭했는지 안했는지 확인
    if event.likes.filter(id=id).exists():
        event.likes.remove(member)
        result = 1
    else:
        event.likes.add(member)
        result = 0 
    count = event.likes.count()
    print('좋아요 개수', count)
    context = {'result':result,'count':count}
    return JsonResponse(context)