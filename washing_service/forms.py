from datetime import datetime
from django.forms import ModelForm, DateTimeInput
from .models import ScheduledOrder


class CreateNewOrder(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateNewOrder, self).__init__(*args, **kwargs)
        self.fields['location'].empty_label = ''
        self.fields['car_type'].empty_label = ''

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
            'car': 'Your Car',
            'phone': 'Phone Number',
        }
