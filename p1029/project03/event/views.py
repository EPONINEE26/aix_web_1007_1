from django.shortcuts import render
from event.models import Event
from comment.models import Comment

def event(request):
    qs = Event.objects.all().order_by('-eno')
    context = {'list':qs}
    return render(request, 'event.html', context)


def eview(request,eno):
    print('확인 : ',eno)
    qs = Event.objects.filter(eno=eno)[0]   
    qs2 = Comment.objects.filter(event=qs).order_by('-cno')
    qs2_count = qs2.count() # 댓글전체개수
    context = {'event':qs, 'commlist':qs2,'count':qs2_count}
    return render(request, 'eview.html', context)