from django.shortcuts import render, redirect
from django.db.models import F, Q
from board.models import Board, Member
import os
from django.http import JsonResponse
from django.conf import settings


# 차트그래프
def chart(request):
    return render(request, 'chart.html')


# ajax통신
def chart_data(request):
    # 수정: 제목 검색값을 word 변수에 저장
    word = request.POST.get('word', '')
    
    # 수정: 조회수 입력값이 비어 있을 경우 0으로 처리
    search = request.POST.get('search', '').strip()
    search = int(search) if search.isdigit() else 0    
    qs = Board.objects.filter(
        Q(btitle__contains=word) | Q(bhit__gte=search)).values()[:6]

    r_qs = list(qs)
    context = {'list': r_qs, 'data1': [], 'data2': '홍길동'}
    return JsonResponse(context)



# 게시글 삭제
def bdelete(request, bno):
    qs = Board.objects.get(bno=bno)
    media_root = settings.MEDIA_ROOT
    remove_file = media_root + "/" + str(qs.bfile)
    if qs.bfile and os.path.isfile(remove_file):
        os.remove(remove_file)
    qs.delete()
    context = {'temp': 0, 'bno': bno}
    return render(request, 'bwrite.html', context)


# 게시글 수정
def bupdate(request, bno):
    if request.method == 'GET':
        qs = Board.objects.get(bno=bno)
        context = {'board': qs}
        return render(request, 'bupdate.html', context)
    elif request.method == 'POST':
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        bfile = request.FILES.get('bfile')
        qs = Board.objects.get(bno=bno)
        qs.btitle = btitle
        qs.bcontent = bcontent
        if bfile:
            qs.bfile = bfile
        qs.save()
        context = {'temp': 2, 'bno': bno}
        return render(request, 'bwrite.html', context)


# 수정: 답변 작성·등록 전 로그인 확인 및 원래 답변 페이지 복귀
# 수정: Board 모델에 없는 member 필드 대신 기존 id 필드 사용
def breply(request, bno):
    if not request.session.get('session_id'):
        request.session['reply_next'] = f'/board/breply/{bno}/'
        return redirect('/member/login/')

    if request.method == 'GET':
        board = Board.objects.get(bno=bno)
        # 수정: 로그인 직후 원본과 동일한 성공 메시지를 한 번만 표시
        login_success = request.session.pop('reply_login_success', False)
        return render(request, 'breply.html', {'board': board, 'login_success': login_success})

    elif request.method == 'POST':
        board = Board.objects.get(bno=bno)
        bgroup = board.bgroup or board.bno
        bstep = board.bstep
        bindent = board.bindent
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        bfile = request.FILES.get('bfile')
        Board.objects.filter(bgroup=bgroup, bstep__gt=bstep).update(bstep=F('bstep') + 1)
        Board.objects.create(
            id=request.session['session_id'], btitle=btitle,
            bcontent=bcontent, bgroup=bgroup, bstep=bstep + 1,
            bindent=bindent + 1, bfile=bfile,
        )
        return redirect('/board/blist/')


# 게시글 리스트
def blist(request):
    qs = Board.objects.all().order_by('-bgroup', 'bstep')
    context = {'list': qs}
    return render(request, 'blist.html', context)


# 게시글 등록
def bwrite(request):
    if request.method == 'GET':
        return render(request, 'bwrite.html')
    elif request.method == 'POST':
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        bfile = request.FILES.get('bfile')
        
        id = request.session.get('session_id')
        if not id:
            return redirect('/member/login/')
        qs = Board.objects.create(id=id, btitle=btitle, bcontent=bcontent, bfile=bfile)
        qs.bgroup = qs.bno
        qs.save()
        context = {'temp': 1}
        return render(request, 'bwrite.html', context)


# 게시글 상세보기
def bview(request, bno):
    qs = Board.objects.filter(bno=bno)
    qs.update(bhit=F('bhit') + 1)
    context = {'board': qs.first()}
    return render(request, 'bview.html', context)