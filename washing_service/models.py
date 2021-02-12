from django.core.validators import MinValueValidator
from django.db import models

from washing_service.validators import (
    validate_gender,
    unique_brand,
    validate_phone
)


class WashingCenter(models.Model):
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.location

    class Meta:
        verbose_name = 'Washing Center'
        verbose_name_plural = 'Washing Centers'


class Manager(models.Model):
    full_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, help_text='Enter M/F',
                              validators=[validate_gender])
    salary = models.IntegerField(help_text='Monthly salary',
                                 validators=[MinValueValidator(0)])
    location = models.OneToOneField(WashingCenter, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Manager'
        verbose_name_plural = 'Managers'


class Washer(models.Model):
    full_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, help_text='Enter M/F',
                              validators=[validate_gender])

    # Washer gets salary per order %
    salary = models.DecimalField(max_digits=4, decimal_places=2,
                                 help_text='Salary per order %',
                                 validators=[MinValueValidator(0)])
    location = models.ForeignKey(WashingCenter, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Washer'
        verbose_name_plural = 'Washers'


class CarType(models.Model):
    type = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=4, decimal_places=2,
                                help_text='Price per wash',
                                validators=[MinValueValidator(0)])

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Car Type'
        verbose_name_plural = 'Car Types'


class CarBrand(models.Model):
    brand = models.CharField(max_length=20, validators=[unique_brand])
    car_logo = models.ImageField(default='default-car.png',
                                 blank=True, null=True)

    def __str__(self):
        return self.brand

    class Meta:
        verbose_name = 'Car Brand'
        verbose_name_plural = 'Car Brands'


class History(models.Model):
    customer = models.CharField(max_length=50)
    location = models.ForeignKey(WashingCenter, on_delete=models.CASCADE)
    car_type = models.ForeignKey(CarType, on_delete=models.CASCADE)
    car_brand = models.ForeignKey(CarBrand, on_delete=models.DO_NOTHING,
                                  blank=True, null=True)
    date = models.DateTimeField()
    phone = models.CharField(max_length=30, validators=[validate_phone])

    washer = models.ForeignKey(Washer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer} - {self.car_type}"

    class Meta:
        verbose_name = 'History'
        verbose_name_plural = 'Histories'


class ScheduledOrder(models.Model):
    customer = models.CharField(max_length=40)
    location = models.ForeignKey(WashingCenter, on_delete=models.CASCADE)
    car_type = models.ForeignKey(CarType, on_delete=models.CASCADE)
    car_brand = models.ForeignKey(CarBrand, on_delete=models.DO_NOTHING,
                                  blank=True, null=True)
    date = models.DateTimeField()
    phone = models.CharField(max_length=30, validators=[validate_phone])

    washer = models.ForeignKey(Washer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer} - {self.car_type} at {self.date}"

    class Meta:
        verbose_name = 'Scheduled Order'
        verbose_name_plural = 'Scheduled Orders'
