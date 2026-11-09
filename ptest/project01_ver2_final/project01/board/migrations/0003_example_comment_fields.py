from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [("board", "0002_comment")]
    operations = [
        migrations.AlterField(model_name="comment", name="member", field=models.ForeignKey(to="member.member", on_delete=django.db.models.deletion.CASCADE, null=True, blank=True)),
        migrations.AddField(model_name="comment", name="display_name", field=models.CharField(max_length=60, blank=True, default="")),
        migrations.AddField(model_name="comment", name="is_example", field=models.BooleanField(default=False)),
    ]
