from django import forms
from . import models

class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.ProjectModel
        fields = ['name']


class TaskForm(forms.ModelForm):
    class Meta:
        model = models.TaskModel
        fields = ['name', 'content','type','expiration_date']