from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from users.forms import UserRegistrationForm


def register(request: WSGIRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!',
                             extra_tags='register')
            return redirect('home')
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})
