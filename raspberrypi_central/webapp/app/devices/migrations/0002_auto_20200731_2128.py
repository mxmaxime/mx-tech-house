# Generated by Django 3.0.7 on 2020-07-31 21:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0001_initial'),
        ('devices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='location',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='house.Location'),
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]
