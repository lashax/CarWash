from django.forms import ModelForm
from django import forms
from .models import ScheduledOrders


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class CreateNewOrder(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateNewOrder, self).__init__(*args, **kwargs)
        self.fields['location'].empty_label = ''

    class Meta:
        model = ScheduledOrders
        fields = ['customer', 'location', 'car', 'phone', 'date']
        widgets = {
            'date': DateTimeInput(),
        }

        labels = {
            'customer': 'Full Name',
            'car': 'Your Car',
            'phone': 'Phone Number',
        }

