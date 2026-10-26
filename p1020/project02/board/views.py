from django.shortcuts import render,redirect
from board.models import Board
from django.db.models import F,Q 
from django.conf import settings
from django.conf.urls.static import static
import os
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# 차트그래프
def chart(request):
    # id_list = ['aaa','bbb','ccc','ddd','eee','fff']
    qs = Board.objects.all().order_by('bno')[:6]
    # qs_value = list(qs.values())
    
    # id_list = [1,2,3,4,5,6]
    # bhit_list = [19,20,21,26,40,70]
    # print(qs.values)
    # context = {'id_list':id_list,'bhit_list':bhit_list,}
    return render(request, 'chart.html')


# ajax 페이지로 이동 
# @csrf_exemp : csrf_token 예외처리
def chart_data(request):
    id_list = ['aaa','bbb','ccc','ddd','eee','fff']
    bhit_list = [19,20,21,26,40,70]
    data = {'id_list':id_list, 'bhit_list':bhit_list}
    
    # db에서 가져와서 차트그래프 그리기 
    
    return JsonResponse(data)


# 게시글 리스트 # 하단넘버링
# GET - 페이지열기, POST - 검색부분
def blist(request):
    if request.method == 'GET':
        qs = Board.objects.all().order_by('-bgroup','bstep')
        paginator = Paginator(qs,5)
        # 현재페이지
        page = int(request.GET.get('page',1)) # 페이지가 넘어오면 그 값, 없을때 1
        p_qs = paginator.get_page(page)

        context = {'list':p_qs,'page':page}  #id->member
        return render(request, 'blist.html',context)
    elif request.method == 'POST':
        category = request.POST.get('category')
        search_word = request.POST.get('search_word')
        # btitle검색
        if category == 'btitle':
            qs = Board.objects.filter(btitle__contains=search_word).order_by('-bgroup','bstep')
        elif category == 'bcontent':
            qs = Board.objects.filter(bcontent__contains=search_word).order_by('-bgroup','bstep')
        else:
            qs = Board.objects.filter\
                (Q(btitle__contains=search_word) | Q(bcontent__contains=search_word)   )\
                .order_by('-bgroup','bstep')

                
            # 번호가 30번 이상이거나 조회수가 50이상인 것 검색    
            # qs = Board.objects.filter(Q(bno__gte = 30)|Q(bhit__lte=50).order_by('-bgroup','bstep'))   
                # print('개수 : ', qs.count)
                
            # 이름에 s자가 있고 조회수가 50이상인 것 검색 
            # qs = Board.objects.filter(Q(id__icontains='s')|Q(bhit__lte=50).order_by('-bgroup','bstep'))   

        paginator = Paginator(qs,5)
        # 현재페이지
        page = int(request.GET.get('page',1)) # 페이지가 넘어오면 그 값, 없을때 1
        p_qs = paginator.get_page(page)

        context = {'list':p_qs,'page':page}  #id->member
        return render(request, 'blist.html',context)
        

        
        
        
        #페이징처리---------------------------------------------
        paginator = Paginator(qs,100) 
        page = int(request.GET.get('page',1))
        qs = paginator.get_page(page)
        #---------------------------------------------
        context = {'list':qs, 'page':page}
        return render(request, 'blist.html',context)





# GET : 페이지 열기, POST : 저장
def bwrite(request):
    if request.method=="GET":    
        return render(request, 'bwrite.html')
    elif request.method=="POST":
        btitle = request.POST.get('btitle')
        id = request.POST.get('id')
        bcontent = request.POST.get('bcontent')
        bfile = request.FILES.get('bfile')
        print(f'데이터확인 : {btitle},{id},{bcontent},{bfile}')
        
        # create 방식 
        qs = Board.objects.create(btitle=btitle,id=id,bcontent=bcontent,bfile=bfile)        

        #답변달기
        qs.bgroup = qs.bno
        qs.save()
        
        # save 방식
        # Board(btitle=btitle,id=id,bcontent=bcontent,bfile=bfile).save()
        context = {'temp':1}
        return render(request, 'bwrite.html',context)
            # return redirect('/board/blist/')

# 게시글 상세보기 
def bview(request,bno):
    # board 1개 검색 
    qs = Board.objects.get(bno=bno)
    # qs.bhit = qs.bhit+1
    # qs.save()
    
    # 데이터 1개 가져오기
    # qs = Board.objects.filter(bno=bno).first() # .first()
    qs = Board.objects.filter(bno=bno)
    qs.update(bhit=F('bhit')+1) # F함수 : qs에 있는 컬럼값을 가져올 때 사용 
    
        
    context = {'board':qs[0]}
    return render(request, 'bview.html',context)

# 게시글 삭제
def bdelete(request,bno):  
    Board.objects.get(bno=bno).delete() 
    context = {'temp':0, 'bno':bno}
    return render(request, 'bwrite.html',context)

# 게시글 수정 
# GET : 수정페이지열기, POST:수정저장 
def bupdate(request,bno): 
    if request.method=="GET":
        qs = Board.objects.get(bno=bno) 
        context = {'board':qs}       
        return render(request, 'bupdate.html',context)
    
    elif request.method=="POST":
        btitle = request.POST.get('btitle')
        # id = request.POST.get('id')
        bcontent = request.POST.get('bcontent')
        bfile = request.FILES.get('bfile')
        # old_file = request.POST.get('old_file')
        qs = Board.objects.get(bno=bno)
        qs.btitle = btitle
        qs.id = id
        qs.bcontent = bcontent
        if bfile:
            qs.bfile = bfile

        qs.save()
        
        context = {'temp':2, 'bno':bno}
        return render(request, 'bwrite.html',context)
        