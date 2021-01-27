# Generated by Django 3.1.5 on 2021-01-27 12:20

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('washing_service', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employees',
            old_name='working_place',
            new_name='location',
        ),
        migrations.RenameField(
            model_name='scheduledorders',
            old_name='place',
            new_name='location',
        ),
        migrations.RenameField(
            model_name='washinghistory',
            old_name='place',
            new_name='location',
        ),
        migrations.RemoveField(
            model_name='washingcenter',
            name='manager',
        ),
        migrations.AddField(
            model_name='scheduledorders',
            name='phone',
            field=models.CharField(default=557773255, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='washinghistory',
            name='phone',
            field=models.CharField(default=datetime.datetime(2021, 1, 27, 12, 20, 51, 368987, tzinfo=utc), max_length=30),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('location', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='washing_service.washingcenter')),
            ],
        ),
    ]
