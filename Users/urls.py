from django.urls import path
from .views import *



urlpatterns = [
    path('auth/login', log_in, name='login'),
    path('auth/register', register, name='register'),
    path('auth/logout', mylogout, name='logout'),

    path('team-list', team_list, name='team_list'),
    path('team-create', team_create, name='team_create'),
    path('team-retrieve-<str:team_prefix>', team_retrieve, name='team_retrieve'),
    path('team-update-data-<str:team_prefix>', team_update, name='team_update'),
    path('team-remove-users-<str:team_prefix>-<int:user_id>', team_remove_users, name='team_remove_users'),
    path('team-add-users-<str:team_prefix>', team_add_users, name='team_add_users'),
    path('team-delete-<str:team_prefix>', team_delete, name='team_delete')
]