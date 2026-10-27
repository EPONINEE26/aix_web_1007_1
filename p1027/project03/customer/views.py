from django.shortcuts import render
from customer.models import Board
from django.utils import timezone
from datetime import timedelta

def clist(request):
    qs = Board.objects.all().order_by('-bgroup','bstep')
    print('확인 :', qs)
    context = {'list':qs}
    return render(request, 'clist.html',context)


def cview(request, bno):
    qs = Board.objects.filter(bno=bno)[0]
    print('확인 :', qs)
    context = {'board': qs}
    return render(request, 'cview.html', context)