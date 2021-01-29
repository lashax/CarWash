from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import CreateNewOrder
from django.urls import reverse
from django.contrib import messages


def home(request):
    if request.method == 'POST':
        form = CreateNewOrder(request.POST)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Your visit has been saved!')
            return HttpResponseRedirect(reverse('home'))
    else:
        form = CreateNewOrder()

    return render(request, 'washing_service/main.html', {'form': form})
