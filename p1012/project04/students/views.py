from django.shortcuts import render,redirect


def swrite(request):
    return render(request,'swrite.html')

def slist(request):
    return render(request,'slist.html')

