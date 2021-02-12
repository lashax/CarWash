from datetime import datetime, timedelta

from django.forms import (ModelForm, DateTimeInput, ModelChoiceField,
                          DateTimeField)
from .models import ScheduledOrder, CarType, WashingCenter, CarBrand

from .validators import validate_date


class CreateNewOrder(ModelForm):
    car_type = ModelChoiceField(queryset=CarType.objects.all(), empty_label='',
                                label='Car Type')
    car_brand = ModelChoiceField(queryset=CarBrand.objects.all(),
                                 empty_label='', label='Car Brand',
                                 required=False)
    location = ModelChoiceField(queryset=WashingCenter.objects.all(),
                                empty_label='')

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
        fields = ['customer', 'location', 'car_type', 'car_brand',
                  'phone', 'date']

        labels = {'customer': 'Full Name'}


class CreateCarBrand(ModelForm):

    class Meta:
        model = CarBrand
        fields = ['brand', 'car_logo']
