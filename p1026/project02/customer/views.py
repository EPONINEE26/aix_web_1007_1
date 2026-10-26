from django.shortcuts import render
from customer.models import Board

def cview(request,bno):
    qs = Board.objects.filter(bno=bno)[0]
    print(f'데이터확인 :', qs)
    context = {'list':qs}
    return render(request, 'cview.html',context)



def clist(request):
    qs = Board.objects.all().order_by('-bgroup','bstep')
    print(f'데이터확인 :', qs)
    context = {'list':qs}
    return render(request, 'clist.html',context)




# html -> Django
# form, url path, 파라미터, 자바스크립트(ajax)
# Django -> html
# context 
