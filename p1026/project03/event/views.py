from django.shortcuts import render


def eview(request, eno):
    print(f'데이터확인 :', eno)
    return render(request, 'eview.html')

def event(request):
    return render(request, 'event.html')

