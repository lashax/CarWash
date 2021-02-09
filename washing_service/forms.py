from datetime import datetime
from django.forms import ModelForm, DateTimeInput, ModelChoiceField
from .models import ScheduledOrder, CarType, WashingCenter


class CreateNewOrder(ModelForm):
    car_type = ModelChoiceField(queryset=CarType.objects.all(), empty_label='',
                                label='Car Type')
    location = ModelChoiceField(queryset=WashingCenter.objects.all(),
                                empty_label='')

    class Meta:
        model = ScheduledOrder
        fields = ['customer', 'location', 'car_type', 'phone', 'date']

        date_attrs = {
            'type': 'datetime-local',
            'min': datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M"),
        }
        widgets = {
            'date': DateTimeInput(attrs=date_attrs),
        }

        labels = {
            'customer': 'Full Name',
            'phone': 'Phone Number',
        }
