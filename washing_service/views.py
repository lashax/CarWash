from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import CreateNewOrder


def home(request):
    if request.method == 'POST':
        form = CreateNewOrder(request.POST)

        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/')
    else:
        form = CreateNewOrder()

    return render(request, 'washing_service/main.html', {'form': form})
