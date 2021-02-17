from random import randint

from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .forms import CreateNewOrder, CreateCarBrand
from .models import CarBrand, Washer
from .view_helpers.washers import earning_by_time


def home(request: WSGIRequest) -> HttpResponse:
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
                                 'Your visit has been saved!',
                                 extra_tags='order')
            return HttpResponseRedirect(f"{reverse('home')}#schedule_form")
    else:
        form = CreateNewOrder()

    return render(request, 'washing_service/home.html', {'form': form})


def washers(request: WSGIRequest) -> HttpResponse:
    paginator = Paginator(Washer.objects.all(), 3,
                          allow_empty_first_page=True)
    page_number = request.GET.get('page')
    washers_page = paginator.get_page(page_number)

    washers_info = {}

    # Each washers' overall salary
    overall = earning_by_time('overall', washers_page)

    # Each washers' salary in the current year
    year = earning_by_time('year', washers_page)

    # Each washers' salary in the current month
    month = earning_by_time('month', washers_page)

    # Each washers' salary in the current week
    week = earning_by_time('week', washers_page)

    for index, washer in enumerate(overall):
        # 'info' list will contain items, in the following order: id,
        # True/False (True if M, False if F), location, overall income,
        # yearly income, monthly income, weekly income.
        info = [washer.id]
        if washer.gender.upper() == 'M':
            info.append(True)
        else:
            info.append(False)
        info.extend([washer.location, overall[index].overall,
                     year[index].year, month[index].month,
                     week[index].week])

        washers_info[washer.full_name] = info

    context = {'washers': washers_info, 'washers_page': washers_page}

    return render(request, 'washing_service/washers.html', context=context)


def cars(request: WSGIRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CreateCarBrand(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'New car brand has been saved!')

            return HttpResponseRedirect(request.session['current_page'])
    else:
        form = CreateCarBrand()

    # Saves current page's path
    request.session['current_page'] = request.path_info + '?page=' \
                                      + request.GET.get('page', '1')

    paginator = Paginator(CarBrand.objects.all(), 9,
                          allow_empty_first_page=True)
    page_number = request.GET.get('page')
    car_brands = paginator.get_page(page_number)
    return render(request, 'washing_service/cars.html',
                  {'car_brands': car_brands, 'form': form})
