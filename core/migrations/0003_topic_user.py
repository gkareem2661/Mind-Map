from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_topic_mind_map_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='user',
            field=models.ForeignKey(blank=True, help_text='Owner of the saved topic', null=True, on_delete=models.CASCADE, related_name='topics', to=settings.AUTH_USER_MODEL),
        ),
    ]

