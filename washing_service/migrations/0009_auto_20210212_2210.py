# Generated by Django 3.1.5 on 2021-02-12 18:10

import django.core.validators
from django.db import migrations, models
import washing_service.validators


class Migration(migrations.Migration):

    dependencies = [
        ('washing_service', '0008_auto_20210212_0149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartype',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='Price per wash', max_digits=4, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='manager',
            name='gender',
            field=models.CharField(help_text='Enter M/F', max_length=1, validators=[washing_service.validators.validate_gender]),
        ),
        migrations.AlterField(
            model_name='manager',
            name='salary',
            field=models.IntegerField(help_text='Monthly salary', validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='washer',
            name='gender',
            field=models.CharField(help_text='Enter M/F', max_length=1, validators=[washing_service.validators.validate_gender]),
        ),
        migrations.AlterField(
            model_name='washer',
            name='salary',
            field=models.DecimalField(decimal_places=2, help_text='Salary per order %', max_digits=4, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
