from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.views.decorators.http import require_POST
from django.db.models import F,Q
from board.models import Board, Comment
from django.core.paginator import Paginator
from django.http import JsonResponse



def board_response(request, url_name, **kwargs):
    url = reverse(url_name, kwargs=kwargs)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'redirect_url': url})
    return redirect(url)


def board_input_error(request, template, context):
    message = '제목과 내용을 입력해 주세요. 제목은 1,000자까지 입력할 수 있습니다.'
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'message': message}, status=400)
    return render(request, template, {**context, 'error': message}, status=400)


def blist(request):
    if request.method == 'GET':
        qs = Board.objects.all().order_by('-bgroup', 'bstep')
        paginaotor = Paginator(qs, 5)
        page = request.GET.get('page', 1)
        p_qs = paginaotor.get_page(page)
        
        context = {'list': p_qs, 'page':page}
        return render(request, 'blist.html', context)
    
    elif request.method == 'POST':
        category = request.POST.get('category')
        search_word = request.POST.get('search_word', '')
        
        if category == 'title':
            qs = Board.objects.filter(btitle__contains=search_word).order_by('-bgroup', 'bstep')
            
        elif category == 'content':
            qs = Board.objects.filter(bcontent__contains=search_word).order_by('-bgroup', 'bstep')                 
        
        else :
            qs = Board.objects.filter(Q(btitle__contains=search_word)|Q(bcontent__contains=search_word)).order_by('-bgroup', 'bstep')
            
        paginator = Paginator(qs, 5) 
        page = request.GET.get('page',1)
        p_qs = paginator.get_page(page) 
        
        context = {'list': p_qs, 'page':page, 'category':category, 'search_word':search_word}
        return render(request, 'blist.html', context)


def bwrite(request):
    id = request.session.get('session_id')
    if not id:
        return redirect(reverse('member:login') + '?login_required=1')

    if request.method == 'POST':
        btitle = request.POST.get('btitle', '').strip()
        bcontent = request.POST.get('bcontent', '')
        bfile = request.FILES.get('bfile')
        if not btitle or len(btitle) > 1000 or not bcontent.strip():
            return board_input_error(request, 'bwrite.html', {})

        with transaction.atomic():
            qs = Board.objects.create(btitle=btitle, id=id, bcontent=bcontent, bfile=bfile)
            qs.bgroup = qs.bno
            qs.save(update_fields=['bgroup'])

        return board_response(request, 'board:blist')

    return render(request, 'bwrite.html')


def bview(request, bno):
    page = int(request.GET.get('page', 1))
    qs = get_object_or_404(Board, bno=bno)
    qs.bhit = qs.bhit + 1
    qs.save()    
     
    pre_qs = Board.objects.filter(Q(bgroup__lt=qs.bgroup, bstep__lte=qs.bstep)|Q(bgroup=qs.bgroup, bstep__gt=qs.bstep)).order_by('-bgroup', 'bstep').first()
    next_qs = Board.objects.filter(Q(bgroup__gt=qs.bgroup,bstep__gte=qs.bstep)|Q(bgroup=qs.bgroup,bstep__lt=qs.bstep)).order_by('-bgroup','bstep').first()

    comments = Comment.objects.filter(Q(board_id=bno) | Q(is_example=True)).order_by('cno').distinct()
    context = {'board': qs, 'pre_board': pre_qs, 'next_board': next_qs, 'page': page, 'comments': comments}
    return render(request, 'bview.html',context)
    
def bupdate(request, bno):
    id = request.session.get('session_id')
    if not id:
        return board_response(request, 'member:login')

    qs = get_object_or_404(Board, bno=bno)
    if qs.id != id:
        raise PermissionDenied

    context = {'board': qs}
    if request.method == 'POST':
        btitle = request.POST.get('btitle', '').strip()
        bcontent = request.POST.get('bcontent', '')
        bfile = request.FILES.get('bfile')
        if not btitle or len(btitle) > 1000 or not bcontent.strip():
            return board_input_error(request, 'bupdate.html', context)

        qs.btitle = btitle
        qs.bcontent = bcontent
        if bfile:
            qs.bfile = bfile
        qs.save()
        return board_response(request, 'board:bview', bno=bno)

    return render(request, 'bupdate.html', context)


@require_POST
def bdelete(request, bno):
    id = request.session.get('session_id')
    if not id:
        return board_response(request, 'member:login')

    qs = get_object_or_404(Board, bno=bno)
    if qs.id != id:
        raise PermissionDenied

    bfile = qs.bfile
    qs.delete()
    if bfile and not Board.objects.filter(bfile=bfile.name).exists():
        bfile.delete(save=False)

    return board_response(request, 'board:blist')


def breply(request, bno):
    id = request.session.get('session_id')
    if not id:
        return board_response(request, 'member:login')

    qs = get_object_or_404(Board, bno=bno)
    context = {'board': qs}

    if request.method == 'POST':
        btitle = request.POST.get('btitle', '').strip()
        bcontent = request.POST.get('bcontent', '')
        bfile = request.FILES.get('bfile')
        if not btitle or len(btitle) > 1000 or not bcontent.strip():
            return board_input_error(request, 'breply.html', context)

        with transaction.atomic():
            qs = Board.objects.select_for_update().get(bno=bno)
            Board.objects.filter(bgroup=qs.bgroup, bstep__gt=qs.bstep).update(
                bstep=F('bstep') + 1
            )
            Board.objects.create(
                btitle=btitle, id=id, bcontent=bcontent, bfile=bfile,
                bgroup=qs.bgroup, bstep=qs.bstep + 1, bindent=qs.bindent + 1,
            )
        return board_response(request, 'board:blist')

    return render(request, 'breply.html', context)


@require_POST
def commWrite(request, bno):
    id = request.session.get('session_id')
    if not id:
        return board_response(request, 'member:login')

    board = get_object_or_404(Board, bno=bno)
    ccontent = request.POST.get('ccontent', '').strip()
    if ccontent:
        Comment.objects.create(board=board, member_id=id, ccontent=ccontent)
    return board_response(request, 'board:bview', bno=bno)


@require_POST
def commUpdate(request, bno, cno):
    id = request.session.get('session_id')
    if not id:
        return board_response(request, 'member:login')

    qs = get_object_or_404(Comment.objects.filter(Q(board_id=bno) | Q(is_example=True)), cno=cno)
    if not qs.is_example and qs.member_id != id:
        return JsonResponse({"message": "작성자만 수정하거나 삭제할 수 있습니다."}, status=403)
    ccontent = request.POST.get('ccontent', '').strip()
    if ccontent:
        qs.ccontent = ccontent
        qs.save(update_fields=['ccontent'])
    return board_response(request, 'board:bview', bno=bno)


@require_POST
def commDelete(request, bno, cno):
    id = request.session.get('session_id')
    if not id:
        return board_response(request, 'member:login')

    qs = get_object_or_404(Comment.objects.filter(Q(board_id=bno) | Q(is_example=True)), cno=cno)
    if not qs.is_example and qs.member_id != id:
        return JsonResponse({"message": "작성자만 수정하거나 삭제할 수 있습니다."}, status=403)
    qs.delete()
    return board_response(request, 'board:bview', bno=bno)


