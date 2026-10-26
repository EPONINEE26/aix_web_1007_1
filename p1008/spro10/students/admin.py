from django.contrib import admin
from django.contrib.admin.views.main import ChangeList

from .models import Stu


class StuAscendingChangeList(ChangeList):
    # 관리자 화면의 기존 정렬 파라미터를 무시하고 번호 오름차순 적용
    def get_ordering(self, request, queryset):
        return (
            'no',
            'pk',
        )


@admin.register(Stu)
class StuAdmin(admin.ModelAdmin):
    # 관리자 목록에 표시할 필드
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

    # 검색 필드
    search_fields = (
        'name',
        'school',
        'sw',
    )

    # 필터 사용 안 함
    list_filter = ()

    # 100명을 한 페이지에 표시
    list_per_page = 100

    # 기본 정렬
    ordering = (
        'no',
        'pk',
    )

    # 사용자 클릭 정렬을 무시하는 ChangeList 사용
    def get_changelist(self, request, **kwargs):
        return StuAscendingChangeList
