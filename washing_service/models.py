from django.db import models


class WashingCenter(models.Model):
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.location

    class Meta:
        verbose_name = 'Washing Center'
        verbose_name_plural = 'Washing Centers'


class Manager(models.Model):
    full_name = models.CharField(max_length=50)
    location = models.OneToOneField(WashingCenter, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Manager'
        verbose_name_plural = 'Managers'


class Washer(models.Model):
    full_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    location = models.ForeignKey(WashingCenter, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Washer'
        verbose_name_plural = 'Washers'


class History(models.Model):
    customer = models.CharField(max_length=50)
    location = models.ForeignKey(WashingCenter, on_delete=models.CASCADE)
    car = models.CharField(max_length=50)
    date = models.DateTimeField()
    phone = models.CharField(max_length=30)

    washer = models.ForeignKey(Washer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer} - {self.car}"

    class Meta:
        verbose_name = 'History'
        verbose_name_plural = 'Histories'


class ScheduledOrder(models.Model):
    customer = models.CharField(max_length=40)
    location = models.ForeignKey(WashingCenter, on_delete=models.CASCADE)
    car = models.CharField(max_length=50)
    date = models.DateTimeField()
    phone = models.CharField(max_length=30)

    washer = models.ForeignKey(Washer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer} - {self.car} at {self.date}"

    class Meta:
        verbose_name = 'Scheduled Order'
        verbose_name_plural = 'Scheduled Orders'
