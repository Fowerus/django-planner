from django import forms
from .models import User, Team
from django.contrib.auth.forms import UserCreationForm



class UserLoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'password')


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('surname', 'first_name', 'second_name', 'email')


class TeamCreateUpdateForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ('name',)