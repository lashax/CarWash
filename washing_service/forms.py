from datetime import datetime, timedelta

from django.forms import (ModelForm, DateTimeInput, ModelChoiceField,
                          DateTimeField, CharField)
from .models import ScheduledOrder, CarType, WashingCenter, CarBrand

from .validators import validate_date, validate_phone, unique_brand


class CreateNewOrder(ModelForm):
    car_type = ModelChoiceField(queryset=CarType.objects.all(), empty_label='',
                                label='Car Type')
    location = ModelChoiceField(queryset=WashingCenter.objects.all(),
                                empty_label='')
    phone = CharField(max_length=30, validators=[validate_phone],
                      label='Phone Number')

    date_attrs = {
        'type': 'datetime-local',
        'min': datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M"),
        'max': datetime.strftime(datetime.now() + timedelta(days=365),
                                 "%Y-%m-%dT%H:%M")
    }
    date = DateTimeField(widget=DateTimeInput(attrs=date_attrs),
                         validators=[validate_date])

    def clean_phone(self):
        """Remove country code (995), + and - from phone number."""
        data = self.cleaned_data['phone']
        data = data.strip(' +').replace('-', '')
        if len(data) == 12:
            data = data[3:]

        return data

    class Meta:
        model = ScheduledOrder
        fields = ['customer', 'location', 'car_type', 'phone', 'date']

        labels = {'customer': 'Full Name'}


class CreateCarBrand(ModelForm):
    brand = CharField(max_length=20, validators=[unique_brand])

    class Meta:
        model = CarBrand
        fields = ['brand', 'car_logo']
