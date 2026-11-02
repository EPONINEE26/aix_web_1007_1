from django.db import models

class Screen(models.Model):
    sno = models.AutoField(primary_key=True)
    rank = models.IntegerField(default=1)  # 순위
    title = models.CharField(max_length=100)  # 영화/콘텐츠 제목
    date = models.DateTimeField(null=True, blank=True)  # 날짜 및 시간, 빈칸 허용 (에러 방지)
    percent = models.FloatField(default=0.0)  # 비율/점유율 (예: 예매율)
    revenue = models.BigIntegerField(default=0)  # 매출액
    crevenue = models.BigIntegerField(default=0)  # 누적 매출액
    sales = models.BigIntegerField(default=0)  # 판매량/관객수
    csales = models.BigIntegerField(default=0)  # 누적 판매량/관객수
        
    def __str__(self):
        return f'{self.sno},{self.rank},{self.title},{self.date},{self.percent},{self.revenue},{self.crevenue},{self.sales},{self.csales}'

# 21억을 넘으면 BigIntegerField()
# FloatField : 소수점
# IntField : 정수 