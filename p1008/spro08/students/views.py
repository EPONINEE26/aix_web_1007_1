from django.shortcuts import render, redirect
from students.models import Stu


def swrite(request):
    # 학생정보 입력 페이지는 GET 요청으로 표시
    if request.method == 'GET':
        return render(request, 'swrite.html')

    # 입력폼에서 저장을 누르면 POST 요청으로 처리
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        major = request.POST.get('major', '').strip()
        grade_text = request.POST.get('grade', '').strip()
        age_text = request.POST.get('age', '').strip()
        gender = request.POST.get('gender', '').strip()

        # grade와 age는 IntegerField이므로 빈 문자열을 그대로 저장하면 오류가 남
        # 입력이 비어 있으면 모델의 기본값과 같은 0을 사용
        try:
            grade = int(grade_text) if grade_text else 0
            age = int(age_text) if age_text else 0
        except ValueError:
            # 숫자가 아닌 값이 전송되면 입력 페이지를 다시 표시
            return render(request, 'swrite.html', {
                'error': '학년과 나이는 숫자로 입력해 주세요.'
            })

        # 기존 Stu 모델과 필드명(name, major, grade, age, gender)을 그대로 사용
        Stu.objects.create(
            name=name,
            major=major,
            grade=grade,
            age=age,
            gender=gender,
        )

        # 저장 후 학생정보 리스트로 이동
        return redirect('students:slist')


def slist(request):
    # 기존 코드는 빈 HTML만 전달해 목록이 표시되지 않았음
    # 데이터베이스에서 학생정보를 읽어 템플릿에 전달합니다.
    students = Stu.objects.all().order_by('id')
    return render(request, 'slist.html', {'students': students})
