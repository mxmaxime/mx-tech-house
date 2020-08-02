# Generated by Django 3.0.7 on 2020-08-02 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_celery_beat', '0012_periodictask_expire_seconds'),
        ('alarm', '0004_auto_20200802_0920'),
    ]

    operations = [
        migrations.AddField(
            model_name='alarmscheduledaterange',
            name='turn_off_task',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alarm_schedule_date_range_off', to='django_celery_beat.PeriodicTask'),
        ),
        migrations.AddField(
            model_name='alarmscheduledaterange',
            name='turn_on_task',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alarm_schedule_date_range_on', to='django_celery_beat.PeriodicTask'),
        ),
        migrations.AlterField(
            model_name='alarmschedule',
            name='friday',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='alarmschedule',
            name='monday',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='alarmschedule',
            name='saturday',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='alarmschedule',
            name='sunday',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='alarmschedule',
            name='thursday',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='alarmschedule',
            name='tuesday',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='alarmschedule',
            name='wednesday',
            field=models.BooleanField(default=False),
        ),
    ]