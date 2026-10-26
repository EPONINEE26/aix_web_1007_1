from django.shortcuts import render,redirect
from django.db.models import F,Q 
from board.models import Board

def blist(request):
    qs = Board.objects.all().order_by('-bgroup','bstep')
    context = {'board':qs}
    return render(request,'blist.html',context)

def bwrite(request):
    if request.method=="GET":
        return render(request,'bwrite.html')
    
    elif request.method=="POST":
        btitle=request.POST.get('btitle')
        id=request.POST.get('id')
        bcontent=request.POST.get('bcontent')
        bfile=request.FILES.get('bfile')
        
        qs = Board.objects.create(btitle=btitle,id=id,bcontent=bcontent,bfile=bfile)
        qs.bgroup = qs.bno
        if qs:
            qs.bfile=bfile
        qs.save()
        
        context = {'temp':1}
        print(f'데이터확인 : {btitle},{id},{bcontent},{bfile}')
        return render(request,'bwrite.html',context)

def bview(request,bno):
    qs = Board.objects.get(bno=bno)
    qs.update(bhit=F('bhit')+1)
    context = {'board':qs[0]}
    return render(request,'bview.html',context)


def bupdate(request,bno):
    if request.method=="GET":
        return render(request,'bupdate.html')
    elif request.method=="POST":
        btitle = request.POST.get('btitle')
        # id = request.POST.get('id')
        bcontent = request.POST.get('bcontent')
        bfile = request.FILES.get('bfile')
        qs = Board.objects.get(bno=bno)
        qs.btitle=btitle
        qs.bcontent=bcontent
        if bfile:
            qs.bfile=bfile
            qs.save()
            context = {'temp':2, 'bno':bno}
            return render(request,'bupdate.html',context)

def bdelete(request,bno):
    Board.objects.get(bno=bno).delete()
    context = {'temp':0,'bno':bno}
    return render(request,'bwrite.html')