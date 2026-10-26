from django.shortcuts import render
from django.http import HttpResponse

def event(request):
    return render(request, 'event.html')