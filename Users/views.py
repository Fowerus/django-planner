from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import *
from .models import Team
from Projects.models import Project



def log_in(request):
    if request.method == 'GET':
        form = UserLoginForm()

        return render(request, 'user_login.html', {'title': 'Login','form': form })

    elif request.method == 'POST':
        form = UserLoginForm(request.POST)
        user = authenticate(request, email=form.data.get('email'),
            password=form.data.get('password'))
        if user is not None:
            login(request, user)

        return redirect('main')


def register(request):
    if request.method == 'GET':
        form = UserRegistrationForm()

        return render(request, 'user_registration.html',
            {'title': 'Registration','form': form })

    elif request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = User(surname=form.cleaned_data['surname'],
                        first_name=form.cleaned_data['first_name'],
                        second_name=form.cleaned_data['second_name'],
                        email=form.cleaned_data['email'])
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, 'Account has been created')

        return render(request, 'user_registration.html',
            {'title': 'Registration','form': form})


@login_required
def mylogout(request):
    logout(request)
    return redirect('main')


@login_required
def team_list(request):
    teams = Team.objects.filter(users=request.user)
    return render(request, 'team.html', {'teams':teams})


@login_required
def team_check(request, team_prefix):
    team = Team.objects.get(prefix=team_prefix)
    if request.user in team.users.all():
        team_projects = Project.objects.filter(team=team)

        return render(request, 'team_retrieve.html', {
                'team':team, 
                'team_projects': team_projects
            })
    return redirect('main')


# @login_required
def team_update(request, team_prefix):
    pass
    # if request.method == 'GET':


    # return redirect('main')   


@login_required
def team_delete(request, team_prefix):
    team = Team.objects.get(prefix=team_prefix)
    if request.user == team.lead:
        team.delete()

    return redirect('team_list')   

