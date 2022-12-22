from django import forms
from .models import *



class ProjectCreationUpdateForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name', 'description')


class TaskCreationForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('name', 'description', 'status', 'priority')