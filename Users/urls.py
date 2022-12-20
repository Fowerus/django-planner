from django.urls import path
from .views import *



urlpatterns = [
    path('auth/login', log_in, name='login'),
    path('auth/register', register, name='register'),
    path('auth/logout', mylogout, name='logout'),

    path('team-list', team_list, name='team_list'),
    path('team-check<str:team_prefix>', team_check, name='team_check'),
    path('team-update-<str:team_prefix>', team_update, name='team_update'),
    path('team-delete-<str:team_prefix>', team_delete, name='team_delete')
]