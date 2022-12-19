from django.urls import path
from .views import *



urlpatterns = [
    path('auth/login', log_in, name='login'),
    path('auth/register', register, name='register')
]