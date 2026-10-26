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

# 차트그래프
def chart(request):
    return render(request, 'chart.html')


def chart_data(request):
    qs = Board.objects.all().order_by('bno')[:6]
    qs_value = list(qs.values())
    data = {'qs_value':qs_value}
    return JsonResponse(data)


def blist(request):
    if request.method == 'GET':
        qs = Board.objects.all().order_by('-bgroup','bstep')

        paginator = Paginator(qs,5) # 5줄씩 리턴
        page = int(request.GET.get('page',1))
        qs = paginator.get_page(page)
  
        context = {'list':qs,'page':page}
        return render(request, 'blist.html',context)
    elif request.method == 'POST':
     
        category = request.POST.get('category')
        search_word = request.POST.get('search_word')
        # category - btitle
        if category == 'btitle':
            qs = Board.objects.filter(btitle__contains=search_word).order_by('-bgroup','bstep')
        elif category == 'bcontent':
            qs = Board.objects.filter(bcontent__contains=search_word).order_by('-bgroup','bstep')
        else:
            qs = Board.objects.filter\
                ( Q(btitle__contains=search_word)|Q(bcontent__contains=search_word) )\
                .order_by('-bgroup','bstep')

        print('개수 : ',qs.count())
        paginator = Paginator(qs,100) # 5줄씩 리턴
        page = int(request.GET.get('page',1))
        qs = paginator.get_page(page)
      
        context = {'list':qs,'page':page}
        return render(request, 'blist.html',context)


def bdelete(request,bno):

    qs = Board.objects.get(bno=bno)
    media_root = settings.MEDIA_ROOT
    remove_file = media_root+"/"+str(qs.bfile)
    if os.path.isfile(remove_file):
        os.remove(remove_file)

    qs.delete()

    context={'temp':0,'bno':bno}
    return render(request, 'bwrite.html',context)

def bupdate(request,bno):
    if request.method =='GET':
        qs = Board.objects.get(bno=bno)
        context = {'board':qs}
        return render(request, 'bupdate.html',context)
    elif request.method == 'POST':
        btitle = request.POST.get('btitle')
        #id = request.POST.get('id')
        bcontent = request.POST.get('bcontent')
        bfile = request.FILES.get('bfile')
        # old_file = request.POST.get('old_file')
        qs = Board.objects.get(bno=bno)
        qs.btitle = btitle
        qs.bcontent = bcontent
        if bfile:
            qs.bfile = bfile
        qs.save()

        context={'temp':2,'bno':bno}
        return render(request, 'bwrite.html',context)


def bwrite(request):
    if request.method == 'GET':
        return render(request, 'bwrite.html')
    elif request.method == 'POST':
        btitle = request.POST.get('btitle')
        id = request.POST.get('id')
        bcontent = request.POST.get('bcontent')
        bfile = request.FILES.get('bfile')
        print(f'데이터확인 : {btitle},{id},{bcontent},{bfile},')
        
        qs = Board.objects.create(btitle=btitle,id=id,bcontent=bcontent,bfile=bfile)

        qs.bgroup = qs.bno
        qs.save()


        # Board(btitle=btitle,id=id,bcontent=bcontent,bfile=bfile).save()
        context = {'temp':1} 
        return render(request, 'bwrite.html', context)

def bview(request,bno):
    qs = Board.objects.filter(bno=bno)  
    qs.update(bhit = F('bhit')+1)  
    
    context = {'board':qs[0]}
    return render(request, 'bview.html',context)

def breply(request, bno):
    if request.method == 'GET':
        qs = Board.objects.get(bno=bno)
        context = {'board': qs}
        return render(request, 'breply.html', context)
    
    elif request.method == 'POST':
        btitle = request.POST.get('btitle')
        id = request.POST.get('id') # 또는 request.session.get('session_id') 등 기존 bwrite 방식과 동일하게 설정
        bcontent = request.POST.get('bcontent')
        bfile = request.FILES.get('bfile')
        
        # 부모글 가져오기
        parent = Board.objects.get(bno=bno)
        bgroup = parent.bgroup
        bstep = parent.bstep
        bindent = parent.bindent
        
        # 같은 그룹 내에서 부모글의 bstep보다 큰 값들의 bstep을 1씩 증가
        Board.objects.filter(bgroup=bgroup, bstep__gt=bstep).update(bstep=F('bstep') + 1)
        
        # 답글 데이터 생성 (부모글의 bgroup 유지, bstep+1, bindent+1)
        Board.objects.create(
            btitle=btitle,
            id=id,
            bcontent=bcontent,
            bfile=bfile,
            bgroup=bgroup,
            bstep=bstep + 1,
            bindent=bindent + 1
        )
        
        context = {'temp': 3}
        return render(request, 'bwrite.html', context)