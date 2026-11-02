# Django 관리자 사이트 기능을 사용하기 위한 admin 모듈.
from django.contrib import admin

# 관리자 목록을 만들 때 Django가 내부적으로 사용하는 ChangeList 클래스.
# 기본 정렬 동작을 바꾸기 위해 상속해서 사용.
from django.contrib.admin.views.main import ChangeList

# 현재 앱의 Stu 모델을 관리자 사이트에 등록하기 위해 가져옴.
from .models import Stu


# ChangeList를 상속하면 관리자 목록 생성 과정을 일부 바꿀 수 있음.
class StuAscendingChangeList(ChangeList):
    # 관리자가 목록을 만들 때 정렬 기준을 결정하는 메서드.
    def get_ordering(self, request, queryset):
        # no를 오름차순으로 정렬하고, 번호가 같으면 pk로 다시 정렬.
        # pk는 각 데이터 행을 구별하는 Django의 기본 키.
        # request와 queryset은 Django가 자동으로 전달하지만 여기서는 정렬 기준만 사용.
        return ('no', 'pk')


# Stu 모델을 관리자 사이트에 등록하고 아래 설정을 적용하는 장식자.
@admin.register(Stu)
class StuAdmin(admin.ModelAdmin):
    # 관리자 목록의 각 행에 보여줄 Stu 필드 이름.
    list_display = (
        'no',
        'name',
        'school',
        'grade',
        'stature',
        'kor',
        'eng',
        'math',
        'sw',
    )

    # 관리자 검색창에 입력한 글자를 비교할 필드.
    search_fields = (
        'name',
        'school',
        'sw',
    )

    # 필터 사이드바를 만들지 않도록 빈 튜플 지정.
    list_filter = ()

    # 관리자 목록에서 한 페이지에 보여줄 최대 행 수.
    list_per_page = 100

    # 관리자가 처음 목록에 들어왔을 때 사용할 정렬 기준.
    ordering = (
        'no',
        'pk',
    )

    # Django가 기본 ChangeList 대신 위에서 만든 정렬 고정 클래스를 사용하게 함.
    def get_changelist(self, request, **kwargs):
        # request와 kwargs는 Django가 호출 규칙에 따라 전달하는 값.
        return StuAscendingChangeList
