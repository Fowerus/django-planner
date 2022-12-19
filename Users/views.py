from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from .forms import *



def log_in(request):
    if request.method == 'GET':
        form = UserLoginForm()

        return render(request, 'user_login.html', {'title': 'Login','form': form })

    elif request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user is not None:
                login(request, user)
        else:
            print(form.errors)

        return redirect('main')


def register(request):
    if request.method == 'GET':
        form = UserRegistrationForm()

        return render(request, 'user_registration.html', {'title': 'Registration','form': form })

    elif request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = User(surname=form.cleaned_data['surname'],
                        first_name=form.cleaned_data['first_name'],
                        second_name=form.cleaned_data['second_name'],
                        email=form.cleaned_data['email'])
            user.set_password(form.cleaned_data['password'])
            user.save()

        return redirect('main')
