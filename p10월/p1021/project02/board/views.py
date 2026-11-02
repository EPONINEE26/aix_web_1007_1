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
    word = request.POST.get('word', '')
    search = request.POST.get('search', 0)
    qs = Board.objects.filter(Q(btitle__contains=word) | Q(bhit__gte=search)).values()[:6]
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


# 답변달기
# 답변달기
def breply(request, bno):
    # 수정부분: 로그인하지 않은 사용자는 로그인 페이지로 이동
    if not request.session.get('session_id'):
        return redirect('/member/login/')

    if request.method == 'GET':
        board = Board.objects.get(bno=bno)
        context = {'board': board}
        return render(request, 'breply.html', context)

    elif request.method == 'POST':
        bgroup = int(request.POST.get('bgroup'))
        bstep = int(request.POST.get('bstep'))
        bindent = int(request.POST.get('bindent'))

        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        bfile = request.FILES.get('bfile')

        member = Member.objects.get(
            id=request.session['session_id']
        )

        Board.objects.filter(
            bgroup=bgroup,
            bstep__gt=bstep
        ).update(
            bstep=F('bstep') + 1
        )

        # 수정부분: member 필드가 아닌 Board의 id 필드에 저장
        Board.objects.create(
            id=member.id,
            btitle=btitle,
            bcontent=bcontent,
            bgroup=bgroup,
            bstep=bstep + 1,
            bindent=bindent + 1,
            bfile=bfile,
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
        
        member = Member.objects.get(id=request.session.get('session_id'))
        qs = Board.objects.create(member=member, btitle=btitle, bcontent=bcontent, bfile=bfile)
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
