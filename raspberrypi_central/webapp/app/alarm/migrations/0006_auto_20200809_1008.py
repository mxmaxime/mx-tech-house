# Generated by Django 3.0.7 on 2020-08-09 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alarm', '0005_auto_20200807_2018'),
    ]

    operations = [
        migrations.CreateModel(
            name='CameraMotionDetectedPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('picture_path', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='cameramotiondetected',
            name='picture_path',
        ),
    ]
