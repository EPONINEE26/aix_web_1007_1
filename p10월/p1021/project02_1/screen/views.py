from django.shortcuts import render
from screen.models import Screen
from django.db.models import F,Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 

def map(request):
    return render(request, 'map.html') 



@csrf_exempt
def chart_data(request):
    search_word = request.POST.get('search_word', "")
    qs = Screen.objects.filter(Q(crevenue__gte=1160000000) | Q(title__contains=search_word)).values()[:6]
    chart_list = list(qs)
    
    context = {"list": chart_list}
    return JsonResponse(context)

def chart(request):
    return render(request,'s_chart.html')


