from django.shortcuts import render, redirect
from students.models import Students

# 학생정보입력, 저장 
def swrite(request):
    if request.method == "GET":
        return render(request,'swrite.html')
    elif request.method == "POST":
        name = request.POST.get('name')
        major = request.POST.get('major')
        age = request.POST.get('age')
        grade = request.POST.get('grade')
        gender = request.POST.get('gender')
        
        qs = Students(name=name,major=major,age=age,grade=grade,gender=gender)
        qs.save()
        print(f'확인 : {name},{major},{age},{grade},{gender}')      
        return render(request,'students/slist.html')

# 학생정보리스트 
def slist(request):
    qs = Students.objects.all()
    context = {'list':qs}
    return render(request, 'slist.html', context)
    
    # return render(request,'slist.html')
    
# 학생상세보기     
def sview(request,name):
    print(f'name 데이터 : {name}')
    qs = Students.objects.get(name=name) # 1개의 정보전송
    context = {'stu': qs}
    return render(request, 'sview.html', context)  

def supdate(request,name):
    if request.method == "GET":            
        print(f'name 데이터 : {name}')
        qs = Students.objects.get(name=name) # 1개의 정보전송
        context = {'stu': qs}
        return render(request, 'supdate.html', context)
    elif request.method == "POST":
        qs = Students.objects.get(name=name) 
        context = {'stu': qs}
        return redirect('/students/slist')

