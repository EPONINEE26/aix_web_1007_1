# HTML 템플릿을 찾아 응답으로 만드는 Django shortcut.
from django.shortcuts import render

def score_write(request):
    # request는 브라우저의 GET 또는 POST 요청 전체를 담은 객체.
    # 현재 함수는 request.method를 확인하지 않고 항상 입력 화면을 반환.
    # 따라서 score_swrite.html의 form이 POST를 보내도 입력값을 읽거나 저장하지 않음.
    # render의 두 번째 인자는 stuscore/templates 안에서 찾을 파일 이름.
    return render(request, 'score_swrite.html')
