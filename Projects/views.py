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


@login_required
def task_main(request, project_prefix):
	try:
		project = Project.objects.get(prefix=project_prefix)
		tasks = project.project_task.all()

		todo = tasks.filter(status='To do')
		in_progress = tasks.filter(status='In progress')
		code_review = tasks.filter(status='Code review')
		done = tasks.filter(status='Done')

		return render(request, 'task/task_main.html', 
			{
				'project':project,
				'todo':todo,
				'in_progress':in_progress,
				'code_review':code_review,
				'done':done
			})

	except:
		return redirect('project_retrieve', project_prefix)


@login_required
def task_retrieve(request, task_id):
	task = Task.objects.get(id=task_id)
	if request.user==task.project.lead or request.user in task.project.team.users.all():

		return render(request, 'task/task_retrieve.html', {
				'task': task
			})
	return redirect('project_list')



@login_required
def task_create(request, project_prefix):
	if request.method == 'POST':
		form = TaskCreationForm(request.POST)
		project = Project.objects.get(prefix=project_prefix)

		if request.user == project.lead:

			if form.is_valid():
				try:
					task = Task(
						name=form.cleaned_data.get('name'),
						description=form.cleaned_data.get('description'),
						status=form.cleaned_data.get('status'),
						creator=request.user,
						priority=form.cleaned_data.get('priority'),
						project=project
						)
					task.save()
					messages.success(request, "Task successfully created")

					return redirect('task_main', project_prefix)
				except:
					messages.error(request, 'Failed to create a new task')

	form = TaskCreationForm()
	return render(request, 'task/task_create.html', {'form':form,
		'project_prefix':project_prefix})


@login_required
def task_add_remove_executor(request, task_id, answer):
	try:
		task = Task.objects.get(id = task_id)
		if request.user == task.project.lead:
			if request.method == 'POST':	
				if answer == 1:
					print(request.POST.get(f'user_email_{task_id}'))
					user = get_user_model().objects.get(email=request.POST.get(f'user_email_{task_id}'))
					if user in task.project.team.users.all():
						task.executor = user
						task.save()
			else:
				if answer != 1:
					task.executor = None
					task.save()

		return redirect('task_main', task.project.prefix)
	except Exception as er:
		print(er)
		return redirect('project_list')


@login_required
def task_accept_delete(request, task_id, answer):
	try:
		task = Task.objects.get(id = task_id)
		if answer == 1:
			if request.user == task.project.lead or request.user == task.executor:
				l = {'To do':'In progress',
				'In progress':'Code review', 'Code review':'Done'}

				if task.status != 'Done':
					task.status = l.get(task.status)
					task.save()
		else:
			if request.user == task.project.lead:
				task.delete()

		return redirect('task_main', task.project.prefix)
	except:
		return redirect('project_list')


@login_required
def task_prev_step(request, task_id):
	try:
		task = Task.objects.get(id = task_id)
		if request.user == task.project.lead:
			l = {'In progress':'To do',
			'Code review':'In progress', 'Done':'Code review'}

			if task.status != 'To do':
				task.status = l.get(task.status)
				task.save()

		return redirect('task_main', task.project.prefix)
	except:
		return redirect('project_list')


@login_required
def project_remove_team(request, project_prefix):
	try:
		project = Project.objects.get(prefix=project_prefix)

		if request.user == project.lead:
			project.team = None
			project.save()

	except:
		pass

	finally:
		return redirect('project_retrieve', project_prefix)