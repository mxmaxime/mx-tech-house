# Generated by Django 3.0.7 on 2020-08-07 11:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notification', '0003_usernotificationsetting'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTelegramBotChatId',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.CharField(max_length=60)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameModel(
            old_name='FreeCarrierUserConf',
            new_name='UserFreeCarrier',
        ),
        migrations.DeleteModel(
            name='UserNotificationSetting',
        ),
    ]