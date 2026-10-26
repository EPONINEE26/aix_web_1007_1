from django.shortcuts import render


def index(request):
    # render: 요청 객체와 템플릿을 합쳐 브라우저에 보낼 HTML 응답 생성.
    # context를 넘기지 않았으므로 index.html은 별도 데이터 없이 출력.
    return render(request, 'index.html')
