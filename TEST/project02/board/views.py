from django.shortcuts import render
from django.db.models import F,Q 
from django.conf import settings
from django.conf.urls.static import static
import os 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from board.models import Board

def blist(request):
    qs = Board.objects.all().order_by('-bgroup','bstep')
    context = {'list':qs}
    return render(request, ' blist.html', context)

def bwrite(request):
    if request.method == "GET":
        return render (request, 'bwrite.html')
    elif request.method == "POST":
        btitle = request.POST.get('btitle')
        id = request.POST.get('id')
        bcontent = request.POST.get('bcontent')
        bfile = request.POST.get('bfile')
        print(f'데이터확인 : {btitle},{id},{bcontent},{bfile}')
        
        qs = Board.objects.create(btitle=btitle, id=id, bcontent=bcontent, bfile=bfile)
        qs.bgroup = qs.bno
        qs.save()
        
        context = {'temp' : '1'}
        return render(request, 'bwrite.html', context)

def bview(request,bno):
    qs = Board.objects.filter(bno=bno)
    qs.update(bhit = F('bhit')+1)
    context = {'board':qs}
    return render (request, 'bview.html', context)

def bupdate(request,bno):
    if request.method == "GET":
        qs = Board.objects.get(bno=bno)
        context = {'board':qs}
        return render (request, 'bupdate.html', context)
    
    elif request.method == "POST":
        btitle = request.POST.get('btitle')
        # id = request.POST.get('id')
        bcontent = request.POST.get('bcontent')
        bfile = request.FILES.get('bfile')
        
        qs = Board.objects.get(bno=bno)
        qs.btitle = btitle
        qs.bcontent = bcontent
        if bfile:
            qs.bfile = bfile 
        qs.save()
        context = {'temp':2, 'bno':bno}
        return render (request, 'bwrite.html', context)

def bdelete(request,bno):
    qs = Board.objects.get(bno=bno)
    
    media_root = settings.MEDIA_ROOT
    remove_file = media_root+"/"+str(qs.bfile)
    if os.path.isfile(remove_file):
        os.remove(remove_file)
        
    qs.delete()
    context = {'temp':0,'bno':bno}
    return render (request, 'bwrite.html', context)

def chart(request):
    return render (request, 'chart.html')

def chart_data(request):
    word = request.POST.get('word','')
    search = request.POST.get('search','')
    print('search':search)
    qs = Board.filter(Q(btitle__contains=word) | Q(bhit__gte=search)).values()[:6]
    print(f'데이터확인 : ', qs)
    print(f'데이터확인 : ', qs.count())
    
    r_qs = list(qs)
    context = {'list':r_qs, 'data1':[1,2,3,4],'data2':'홍길동'}
    return JsonResponse(context)