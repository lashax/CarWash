# Generated by Django 3.1.5 on 2021-01-29 22:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('washing_service', '0007_merge_20210130_0243'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Employees',
            new_name='Employee',
        ),
        migrations.RenameModel(
            old_name='ScheduledOrders',
            new_name='ScheduledOrder',
        ),
    ]
