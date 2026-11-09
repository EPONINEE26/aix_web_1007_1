from django.db import migrations
from datetime import datetime
from django.utils import timezone

def add_reference_comments(apps, schema_editor):
    Board = apps.get_model('board', 'Board')
    Comment = apps.get_model('board', 'Comment')
    board = Board.objects.order_by('bno').first()
    if not board:
        return
    examples = [
        ('홍길동', '2026-09-15 14:30', '가을 패키지가 정말 기대됩니다.\n좋은 정보 감사합니다.'),
        ('김민수', '2026-09-15 13:15', '가족들과 방문할 예정인데\n좋은 프로그램이 많네요.'),
        ('이수진', '2026-09-14 18:20', '다음 달에 예약하려고 합니다.\n이용 기간을 확인해봐야겠네요.'),
    ]
    for name, when, content in examples:
        if not Comment.objects.filter(board_id=board.pk, display_name=name, ccontent=content, is_example=True).exists():
            obj = Comment.objects.create(board_id=board.pk, display_name=name, ccontent=content, is_example=True)
            Comment.objects.filter(pk=obj.pk).update(cdate=timezone.make_aware(datetime.strptime(when, '%Y-%m-%d %H:%M')))

class Migration(migrations.Migration):
    dependencies = [('board', '0003_example_comment_fields')]
    operations = [migrations.RunPython(add_reference_comments, migrations.RunPython.noop)]
