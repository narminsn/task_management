from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.ProjectModel)
admin.site.register(models.TaskModel)