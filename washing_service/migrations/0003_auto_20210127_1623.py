# Generated by Django 3.1.5 on 2021-01-27 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('washing_service', '0002_auto_20210127_1620'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='WashingHistory',
            new_name='History',
        ),
    ]
