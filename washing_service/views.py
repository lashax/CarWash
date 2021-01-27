from django.shortcuts import render


def home(request):
    return render(request, 'washing_service/main.html')
