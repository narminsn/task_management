from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ProjectModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class TaskModel(models.Model):
    project = models.ForeignKey('ProjectModel',null=True, on_delete=models.CASCADE)
    type_choices = [
        ('daily','daily'),
        ('weekly', 'weekly'),
        ('monthly', 'monthly'),
        ('one time','one time')
    ]
    status_choices = [
        ('pause','pause'),
        ('in progress','in progress'),
        ('done', 'done'),
        # ('monthly', 'monthly'),
        # ('one time','one time')
    ]
    name = models.CharField(max_length=255)
    content = models.TextField()
    expiration_date = models.DateTimeField(max_length=255)
    type = models.CharField(max_length=255,choices=type_choices)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    status = models.CharField(max_length=255,choices=status_choices,null=True)

    def __str__(self):
        return self.name