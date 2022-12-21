from django.urls import path
from .views import *



urlpatterns = [
    path('project-list', project_list, name='project_list'),
    path('project-create', project_create, name='project_create'),
    path('project-retrieve-<str:project_prefix>', project_retrieve, name='project_retrieve'),
    path('project-update-data-<str:project_prefix>', project_update, name='project_update'),
    path('project-delete-<str:project_prefix>', project_delete, name='project_delete'),
]