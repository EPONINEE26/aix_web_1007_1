from django.shortcuts import render

def index(requdest):
    return render(requdest, 'index.html')
