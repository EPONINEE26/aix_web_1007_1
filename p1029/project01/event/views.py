from django.shortcuts import render
from event.models import Event
from comment.models import Comment

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
