from django.shortcuts import render

def bdelete(request):
    return render(request, 'blist.html')

def bupdate(request):
    return render(request, 'blist.html')

def bview(request):
    return render(request, 'blist.html')

def bwrite(request):
    return render(request, 'blist.html')

def blist(request):
    return render(request, 'blist.html')
