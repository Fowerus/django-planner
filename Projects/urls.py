from django.urls import path
from .views import *



urlpatterns = [
    path('project-list', project_list, name='project_list'),
    path('project-create', project_create, name='project_create'),
    path('project-retrieve-<str:project_prefix>', project_retrieve, name='project_retrieve'),
    path('project-update-data-<str:project_prefix>', project_update, name='project_update'),
    path('project-delete-<str:project_prefix>', project_delete, name='project_delete'),
    path('project-remove-team-<str:project_prefix>', project_remove_team, name='project_remove_team'),

    path('task-main-<str:project_prefix>', task_main, name='task_main'),
    path('task-create-<str:project_prefix>', task_create, name='task_create'),
    path('task-retrieve-<int:task_id>', task_retrieve, name='task_retrieve'),
    path('task-add-remove-executor-<int:task_id>-<int:answer>', task_add_remove_executor, name='task_add_remove_executor'),
    path('task-accept-delete-<int:task_id>-<int:answer>', task_accept_delete, name='task_accept_delete'),
    path('task-prev-step-<int:task_id>', task_prev_step, name='task_prev_step'),
]