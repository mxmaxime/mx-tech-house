# Generated by Django 3.0.7 on 2020-11-06 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0002_auto_20200731_2128'),
        ('alarm', '0023_remove_cameramotiondetectedpicture_picture_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='camerarectangleroi',
            name='definition_height',
        ),
        migrations.RemoveField(
            model_name='camerarectangleroi',
            name='definition_width',
        ),
        migrations.RemoveField(
            model_name='camerarectangleroi',
            name='device',
        ),
        migrations.CreateModel(
            name='CameraROI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('define_picture', models.ImageField(upload_to='')),
                ('device', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='devices.Device')),
            ],
        ),
        migrations.AddField(
            model_name='camerarectangleroi',
            name='camera_roi',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='alarm.CameraROI'),
            preserve_default=False,
        ),
    ]
