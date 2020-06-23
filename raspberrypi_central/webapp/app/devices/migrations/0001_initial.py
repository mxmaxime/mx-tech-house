# Generated by Django 3.0.2 on 2020-02-01 14:16

import devices.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AlertType',
            fields=[
                ('type', models.CharField(max_length=60, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('bucket_name', models.CharField(max_length=60)),
                ('object_name', models.CharField(max_length=100)),
                ('storage_type', models.IntegerField(choices=[(0, 'Amazon s3')])),
            ],
        ),
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('type', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('structure', models.CharField(max_length=60)),
                ('sub_structure', models.CharField(max_length=60)),
            ],
            options={
                'unique_together': {('structure', 'sub_structure')},
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, unique=True)),
                ('device_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='devices.DeviceType')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='devices.Location')),
            ],
        ),
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('severity', models.CharField(choices=[(devices.models.SeverityChoice['LOW'], 'low'), (devices.models.SeverityChoice['MODERATE'], 'moderate'), (devices.models.SeverityChoice['HIGH'], 'high')], max_length=10)),
                ('created_at', models.DateTimeField(editable=False)),
                ('alert_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='devices.AlertType')),
                ('attachments', models.ManyToManyField(blank=True, to='devices.Attachment')),
                ('devices', models.ManyToManyField(blank=True, to='devices.Device')),
            ],
        ),
    ]