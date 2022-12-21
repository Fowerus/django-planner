from django import forms
from .models import *



class ProjectCreationUpdateForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name', 'description')