from random import randint
from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from .forms import CreateNewOrder
from .models import Washer


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

    return render(request, 'washing_service/home.html', {'form': form})


def washers(request):
    wash = {}
    for washer in Washer.objects.all():
        info = [washer.id]
        if washer.gender.upper() == 'M':
            info.append(True)
        else:
            info.append(False)
        info.append(washer.location)

        # ვთვლი, რომ თითო გარეცხვაზე მრეცხავი იღებს 10 ლარს

        # Overall
        info.append(10 * washer.history_set.all().count())

        # Year
        year = datetime.now().year
        info.append(10 * washer.history_set.filter(date__year=year).count())

        # Month
        month = datetime.now().month
        info.append(10 * washer.history_set.filter(date__month=month).count())

        # Week
        week = datetime.now().isocalendar()[1]
        info.append(10 * washer.history_set.filter(date__week=week).count())

        wash[washer.full_name] = info

    context = {'washers': wash}

    return render(request, 'washing_service/washers.html', context=context)