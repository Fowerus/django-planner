from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import *
from .models import *
from Projects.models import Project



@login_required
def project_list(request):
	projects = Project.objects.filter(lead=request.user)
	return render(request, 'project/project_list.html', {'projects':projects})


@login_required
def project_create(request):
	if request.method == 'POST':
		form = ProjectCreationUpdateForm(request.POST)

		if form.is_valid():
			try:
				project = Project(
					name=form.cleaned_data.get('name'),
					description=form.cleaned_data.get('description'),
					lead=request.user
					)
				project.save()
				messages.success(request, "Project successfully created")

				return redirect('project_update', project.prefix)
			except:
				messages.error(request, 'Failed to create a new project')


	form = ProjectCreationUpdateForm()
	return render(request, 'project/project_create.html', {'form':form})


@login_required
def project_retrieve(request, project_prefix):
	project = Project.objects.get(prefix=project_prefix)
	if (project.team and request.user in project.team.users.all()) or request.user == project.lead:

		return render(request, 'project/project_retrieve.html', {
				'project': project
			})
	return redirect('project_list')


@login_required
def project_update(request, project_prefix):
    project = Project.objects.get(prefix=project_prefix)
    prefix = project.prefix
    if request.user == project.lead:
        if request.method == 'GET':
            form = ProjectCreationUpdateForm()

            return render(request, 'project/project_update.html', {'form':form, 'project':project})
        
        elif request.method == 'POST':
            form = ProjectCreationUpdateForm(request.POST)

            try:
                project.name = form.data['name']
                project.description = form.data['description']
                project.save()
                messages.success(request, "Project data successfully changed")
                prefix = project.prefix
            except:
                messages.error(request, "Failed to change project data")

    return redirect('project_update', prefix)


@login_required
def project_delete(request, project_prefix):
    project = Project.objects.get(prefix=project_prefix)
    if request.user == project.lead:
        project.delete()

    return redirect('project_list')   