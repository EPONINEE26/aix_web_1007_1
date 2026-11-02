from django.shortcuts import render
from screen.models import Screen
from django.db.models import F,Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# 카카오맵 ------------------------------------------------
def map(request):
    return render(request,'map.html')


# 차트그래프-------------------------------------------------
def chart(request):
    return render(request,'s_chart.html')

# 차트그래프 - ajax통신
def chart_data(request):
    # 수정: 검색어가 없을 때 영화 목록이 한 개로 제한되지 않도록 조회
    search_word = request.POST.get('search_word', '').strip()
    search = request.POST.get('search', '').strip()
    qs = Screen.objects.all()
    if search_word:
        qs = qs.filter(title__contains=search_word)
    if search:
        try:
            qs = qs.filter(crevenue__gte=int(search))
        except ValueError:
            pass
    # 수정: 차트에서 사용하는 필드만 JSON으로 반환 (기존 검색 조건 유지)
    qs = qs.order_by('rank', 'sno').values('title', 'crevenue')[:6]
    r_qs = list(qs)
    context = {'list':r_qs}
    return JsonResponse(context)
# ------------------------------------------------------------