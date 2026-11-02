from django.shortcuts import render, redirect
from django.db.models import F, Q
from board.models import Board
from django.conf import settings
from django.conf.urls.static import static
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from screen.models import Screen


# 차트그래프 페이지 렌더링
def chart(request): 
    return render(request, 's_chart.html')

# ajax통신
from django.shortcuts import render, redirect
from django.db.models import F, Q
from board.models import Board
from django.http import JsonResponse

# 카카오맵 
def map(request): 
    return render(request, 'map.html')

# 차트그래프 
def chart(request): 
    return render(request, 's_chart.html')

# ajax통신
def chart_data(request):
    search_word=request.POST.get('search_word')
    qs = Screen.objects.filter(Q(crevenue__gte=1160000000)|Q(title__contains='가')).values()[:6]
    r_qs = list(qs)
    context = {'list':r_qs}
    return JsonResponse(context)
 


# # AJAX 비동기 통신으로 차트 데이터 전송
# def chart_data(request):
    # search = request.POST.get('search', '')
    # word = request.POST.get('word', '')
    # print('search:', search, 'word:', word)   
    
    # # 기본 쿼리셋
    # qs = Screen.objects.all()
    
    # # # 1. 제목 검색어(word)가 입력된 경우
    # if word:
    #     qs = qs.filter(Q(title__contains=word))
        
    # # # 2. 숫자 검색값(search)이 입력된 경우 (예: 관객수나 매출액 기준, 여기서는 sales 혹은 crevenue 등 상황에 맞게 변경 가능)
    # # # 만약 search가 비어있지 않고 숫자라면 필터 추가
    # if search and search.isdigit():
    #     qs = qs.filter(Q(crevenue__gte=int(search))) # 또는 sales__gte 등 원하시는 필드 사용

    # # qs = Board.objects.filter(Q(btitle__contains=word) | Q(bhit__gte=search) ).values()[:6]
    # # # 최종적으로 6개만 자르기
    # qs = qs.values()[:6]
    
    # print("데이터 확인 : ", qs)
    # print("데이터 개수 : ", qs.count())
    
    # r_qs = list(qs)
    # context = {'list': r_qs}
    # return JsonResponse(context)



# def chart_data(request):
#     # qs = Board.objects.get(bno=3).values()      # set타입
#     # qs = Board.objects.all().values()         # [] 리스트형태
#     # 제목에 사진글자가 포함되어 있거나 또는 조회수가 70이상인것을 검색하시오.

#     search = request.POST.get('search',0)
#     word = request.POST.get('word',0)
#     print('search : ',search, 'word : ',word)
#     qs = Board.objects.filter(Q(btitle__contains=word) |\

#                             Q(bhit__gte=search) ).values()[:6] # [] 리스트형태

#     print("데이터 확인 : ",qs)
#     print("데이터 개수 : ",qs.count())

#     # 객체를 리스트타입으로 변경해서 보내야 함.
#     r_qs = list(qs)
#     context = {'list':r_qs,'data1':[1,2,3,4],'data2':'홍길동'}
#     return JsonResponse(context)