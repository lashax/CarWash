from django.forms import ModelForm, DateTimeInput
from .models import ScheduledOrder
from datetime import datetime


class CreateNewOrder(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateNewOrder, self).__init__(*args, **kwargs)
        self.fields['location'].empty_label = ''

    class Meta:
        model = ScheduledOrder
        fields = ['customer', 'location', 'car', 'phone', 'date']

        attrs = {
            'type': 'datetime-local',
            'min': datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M"),
        }
        widgets = {
            'date': DateTimeInput(attrs=attrs),
        }

        labels = {
            'customer': 'Full Name',
            'car': 'Your Car',
            'phone': 'Phone Number',
        }
