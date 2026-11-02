# from django.shortcuts import render

# def clist(request):
#     qs = Board.objects.all().order_by('-bgroup','bstep')
#     # 1일 확인 :new아이콘 추가
#     now = timezone.now()
#     for board in qs:
#         board.is_new = (
#             board.bdate >= now - timedelta(days=1)
#             and board.bdate <= now
#         )
#     print('확인 : ',qs)
#     context = {'list':qs}
#     return render(request, 'clist.html',context)

# def cview(request,bno):
#     qs = Board.objects.filter(bno=bno)[0]
#     print('확인 : ',qs)
#     context = {'board':qs}
#     return render(request, 'cview.html',context)
# =================================================================

from django.shortcuts import render
from customer.models import Board   # [추가] Board 모델 불러오기 (이게 없어서 NameError: name 'Board' is not defined 발생)
from django.utils import timezone   # [추가] timezone.now() 사용하려면 필요 (원본에 없었음)
from datetime import timedelta      # [추가] timedelta(days=1) 사용하려면 필요 (원본에 없었음)

def clist(request):
    qs = Board.objects.all().order_by('-bgroup','bstep')
    # 1일 확인 :new아이콘 추가
    now = timezone.now()
    for board in qs:
        board.is_new = (
            board.bdate >= now - timedelta(days=1)
            and board.bdate <= now
        )
    print('확인 : ',qs)
    context = {'list':qs}
    return render(request, 'clist.html',context)

def cview(request,bno):
    qs = Board.objects.filter(bno=bno)[0]
    print('확인 : ',qs)
    context = {'board':qs}
    return render(request, 'cview.html',context)