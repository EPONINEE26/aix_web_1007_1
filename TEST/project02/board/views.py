from django.shortcuts import render,redirect
from django.db.models import F,Q
from board.models import Board
from django.conf import settings
from django.conf.urls.static import static
import os
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from member.models import Member


def blist(request):
    if request.method == "GET":
        qs = Board.objects.all().order_by('-bgroup','bstep')
        paginator = Paginator(qs,5)
        page = int(request.GET.get('page',1))
        context = {'list':qs, 'page':page}
        return render(request, 'blist.html', conext)
    elif request.method == "POST":
        category = request.POST.get('category')
        search_word = request.POST.get('search_word')
        if category == 'btitle':
            qs = Board.objects.filter(btitle__contains=search_word).order_by('-bgroup', 'bstep')
        elif category == 'bcontent':
            qs = Board.objects.filter(bcontent__contains=search_word).order_by('-bgroup', 'bstep')
        else:
            qs = Board.objects.filter(Q(btitle__contains==search_word)|Q(bcontent__contains=search_word)).order_by('-bgroup', 'bstep')
        
        print('개수 : ', qs.count())
        paginator = Paginator(qs,100)
        page = int(request.GET.get('page',1))
        qs = paginator.get_page(page)
        
        context = {'list':qs, 'page':page}
        return render(request, 'blist.html', context)


def bwrite(request):
    if request.method == "GET":
        return render(request, 'bwrite.html')
    elif request.method == "POST":
        btitle = request.POST.get('btitle')
        id = request.POST.get('id')
        bcontent = request.POST.get('bcontent')
        bfile = request.POST.get('bfile')
        
        print(f'데이터확인: {btitle},{id},{bcontent},{bfile}')
        
        qs = Board.objects.create(btitle=btitle,id=id,bcontent=bcontent,bfile=bfile)
        qs.bgroup = qs.bno
        qs.save()       
        
        context = {'temp':1}
        return render(request, 'bwrite.html', context)


def bview(request,bno):
    qs = Board.objects.filter(bno=bno)
    qs.update(bhit = F('bhit')+1)
    context = {'temp':qs[0]}
    return render(request, 'bview.html', context)


def bupdate(request,bno):
    if request.method == "GET":
        qs = Board.objects.get(bno=bno)
        context = {'board':qs}
        return render(request, 'bupdate.html', context)
    elif request.method == "POST":
        btitle = request.POST.get('btitle')
        id = request.POST.get('id')
        bcontent = request.POST.get('bcontent')
        bfile = request.FILES.get('bfile')
        
        qs = Board.objects.get(bno=bno)
        qs.btitle = btitle
        qs.bcontent = bcontent
        if bfile: 
            qs.bfile = bfile 
        qs.save()

        context = {'temp':2, 'bno':bno}
        return render(request,'bwrite.html', context)
        
def bdelete(request,bno):
    qs = Board.objects.get(bno=bno)
    media_root = settings.MEDIA_ROOT
    remove.file = media_root+"/"+str(qs.bfile)
    if os.path.isfile(remove_file):
        os.remove(remove_file)
    qs.delete()
    context = {'temp':0, 'bno':bno}
    return render(request, 'bwrite.html', context)


def breply(request,bno):
    if request.method == "GET":
        qs = Board.objects.get(bno=bno)
        context = {'board':qs}
        return render(request, 'bwrite.html', conext)
    elif request.method == "POST":
        btitle = request.POST.get('btitle')
        id = request.POST.get('id')
        bcontent = request.POST.get('bcontent')
        bfile = request.FILES.get('bfile')
        
        parent = Board.objects.get(bno=bno)
        bgroupt = parent.bgroup
        bstep = parent.bstep
        bindent = parent.bindent
        
        Board.objects.filter(bgroup=bgroup, bstep__gte=bstep).update(bstep=F(bstep)+1)
        
        Board.objects.create(btitle=btitle,id=id,bcontent=bcontent,bgroup=bgroup,bstep=bstep+1,bindent=bindente+1)
        context = {'temp' : 3} # 3을 사용한 가장 합리적인 설계상 이유는 기존 상태값과 충돌하지 않도록 새로운 번호를 배정하기 위함
        return render(request,'bwrite.html', context)