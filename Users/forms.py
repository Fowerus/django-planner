from django import forms
from .models import User



class UserLoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'password')


class UserRegistrationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('surname', 'first_name', 'second_name', 'email', 'password')