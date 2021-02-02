from random import randint

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import CreateNewOrder
from .view_helpers.washers import earning_by_time


def home(request):
    if request.method == 'POST':
        form = CreateNewOrder(request.POST)

        if form.is_valid():
            order = form.save(commit=False)

            # მრეცხავები შეკვეთის ლოკაციის მიხედვით
            loc_washers = order.location.washer_set.all()

            # რენდომად ენიჭება ერთ-ერთ მრეცხავს მოცემული შეკვეთა
            washer = loc_washers[randint(0, len(loc_washers) - 1)]

            order.washer = washer
            order.save()

            messages.add_message(request, messages.SUCCESS,
                                 'Your visit has been saved!')
            return HttpResponseRedirect(f"{reverse('home')}#schedule_form")
    else:
        form = CreateNewOrder()

    return render(request, 'washing_service/home.html', {'form': form})


def washers(request):
    wash = {}

    # Each washers' overall salary
    overall = earning_by_time('overall')

    # Each washers' salary in the current year
    year = earning_by_time('year')

    # Each washers' salary in the current month
    month = earning_by_time('month')

    # Each washers' salary in the current week
    week = earning_by_time('week')

    for index, washer in enumerate(overall):
        info = [washer.id]
        if washer.gender.upper() == 'M':
            info.append(True)
        else:
            info.append(False)
        info.extend([washer.location, int(overall[index].overall),
                     int(year[index].year), int(month[index].month),
                     int(week[index].week)])

        wash[washer.full_name] = info

    context = {'washers': wash}

    return render(request, 'washing_service/washers.html', context=context)
