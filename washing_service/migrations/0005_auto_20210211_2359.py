# Generated by Django 3.1.5 on 2021-02-11 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('washing_service', '0004_auto_20210211_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carbrand',
            name='car_logo',
            field=models.ImageField(blank=True, default='default-car.png', null=True, upload_to=''),
        ),
    ]
