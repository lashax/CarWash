from random import randint
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from .forms import CreateNewOrder


def home(request):
    if request.method == 'POST':
        form = CreateNewOrder(request.POST)

        if form.is_valid():
            order = form.save(commit=False)

            # მრეცხავები შეკვეთის ლოკაციის მიხედვით
            loc_washers = order.location.washer_set.all()

            # რენდომად ენიჭება ერთ-ერთ მრეცხავს მოცემული შეკვეთა
            washer = loc_washers[randint(0, len(loc_washers)-1)]

            order.washer = washer
            order.save()

            messages.add_message(request, messages.SUCCESS,
                                 'Your visit has been saved!')
            return HttpResponseRedirect(f"{reverse('home')}#schedule_form")
    else:
        form = CreateNewOrder()

    return render(request, 'washing_service/main.html', {'form': form})
