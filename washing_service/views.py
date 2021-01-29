from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import CreateNewList
from .models import WashingCenter


def home(request):
    if request.method == 'POST':
        form = CreateNewList(request.POST)

        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/')
    else:
        form = CreateNewList()

    return render(request, 'washing_service/main.html', {'form': form})


def create(request):
    if request.method == 'POST':
        form = CreateNewList(request.POST)
        form.save()
    else:
        form = CreateNewList()
    return render(request, 'washing_service/create.html', {'form': form})
