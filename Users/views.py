from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import *
from .models import Team, Proposal
from Projects.models import Project



def log_in(request):
    if request.method == 'GET':
        form = UserLoginForm()

        return render(request, 'auth/user_login.html', {'title': 'Login','form': form })

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

    return render(request, 'auth/user_registration.html',
        {'title': 'Registration','form': form})


@login_required
def mylogout(request):
    logout(request)
    return redirect('main')


@login_required
def team_list(request):
    teams = Team.objects.filter(users=request.user)
    return render(request, 'team/team_list.html', {'teams':teams})


@login_required
def team_create(request):
    if request.method == 'POST':
        form = TeamCreateUpdateForm(request.POST)

        try:
            team = Team(name=form.data['name'], lead=request.user)
            team.save()
            team.users.add(request.user)
            team.save()
            messages.success(request, "Team successfully created")

            return redirect('team_update', team.prefix)
        except:
            messages.error(request, "Failed to create team")

    form = TeamCreateUpdateForm()
    return render(request, 'team/team_create.html', {'form':form})



@login_required
def team_retrieve(request, team_prefix):
    team = Team.objects.get(prefix=team_prefix)
    if request.user in team.users.all():
        team_projects = Project.objects.filter(team=team)

        return render(request, 'team/team_retrieve.html', {
                'team':team, 
                'team_projects': team_projects
            })
    return redirect('main')


@login_required
def team_update(request, team_prefix):
    team = Team.objects.get(prefix=team_prefix)
    prefix = team.prefix
    if request.user == team.lead:
        if request.method == 'GET':
            form = TeamCreateUpdateForm()

            return render(request, 'team/team_update.html', {'form':form, 'team':team})
        
        elif request.method == 'POST':
            form = TeamCreateUpdateForm(request.POST)

            try:
                team.name = form.data['name']
                team.save()
                messages.success(request, "Team's name successfully changed")
                prefix = team.prefix
            except:
                messages.error(request, "The team's name already taken")

    return redirect('team_update', prefix)


@login_required
def team_remove_users(request, team_prefix, user_id):
    team = Team.objects.get(prefix=team_prefix)
    if request.user == team.lead:
        user = User.objects.get(id=user_id)
        if request.user != user:
            try:
                team.users.remove(user)
                team.save()
                messages.success(request, f'Teammate {user.get_short_name()} successfully removed from team') 
            except:
                messages.error(request, f'Teammate {user.get_short_name()} not removed from team') 

    return redirect('team_update', team_prefix)


@login_required
def team_add_users(request, team_prefix):
    if request.method == 'POST':
        team = Team.objects.get(prefix=team_prefix)
        if request.user == team.lead:
            user = User.objects.get(email=request.POST.get('user_email'))
            if user not in team.users.all():
                try:
                    team.users.add(user)
                    team.save()
                    messages.success(request, f'Teammate {user.get_short_name()} ({user.email}) successfully added to team') 
                except:
                    messages.error(request, f'Teammate {user.get_short_name()} ({user.email}) not added to team') 

    return redirect('team_update', team_prefix)


@login_required
def team_delete(request, team_prefix):
    team = Team.objects.get(prefix=team_prefix)
    if request.user == team.lead:
        team.delete()

    return redirect('team_list')   


@login_required
def proposal_list(request):
    proposals = Proposal.objects.filter(team__lead=request.user)
    
    return render(request, 'proposal/proposal_list.html', {'proposals':proposals})


@login_required
def proposal_accept_decline(request, prop_id, answer):
    try:
        proposal = Proposal.objects.get(id = prop_id)
        if request.user == proposal.team.lead:
            if answer == 1:
                proposal.project.team = proposal.team
                proposal.project.save()
                messages.success(request, 'Proposal accepted')
            else:
                messages.error(request, 'Proposal declined')
            proposal.delete()
    except:
        messages.error(request, 'Failed to accept or decline proposal')

    return redirect('proposal_list')


@login_required
def proposal_send(request, project_prefix):
    if request.method == 'POST':
        try:
            project = Project.objects.get(prefix=project_prefix)
            if request.user == project.lead:
                team = Team.objects.get(prefix=request.POST.get('team_prefix'))

                proposal = Proposal(project=project, team=team)
                proposal.save()
                messages.success(request, 'Proposal successfully sent')

        except:
            messages.error(request, 'Failed to send proposal')

    return redirect('project_retrieve', project_prefix)



