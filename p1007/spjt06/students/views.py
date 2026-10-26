from django.shortcuts import render

# Create your views here.
def swrite(request):
    return render(request,'swrite.html') # render : html을 불러오겠다는 의미 
def slist(request):
    return render(request,'slist.html') # render : html을 불러오겠다는 의미 
