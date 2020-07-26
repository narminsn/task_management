from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.edit import ModelFormMixin
# Create your views here.
from django.contrib.auth.models import User
from . import forms
from django.http import HttpResponse, JsonResponse, QueryDict
from . import models
from django.contrib import messages
from .tasks import  send_mail

class DashboardView(generic.ListView,ModelFormMixin):
    template_name = 'apps_scrumboard.html'
    model = models.ProjectModel
    form_class = forms.ProjectForm
    # context_object_name = 'new_apps_list'

    def get_context_data(self, **kwargs):
        self.object = None
        context = super(DashboardView, self).get_context_data(**kwargs)
        # context['version'] = ApplicationVersion.objects.all()
        context['form'] = self.form_class
        context['task_form'] = forms.TaskForm
        context['tasks'] = models.TaskModel.objects.all()
        return context

    def post(self,request,*args,**kwargs):
        self.object = None

        if 'task' in request.POST:

            id = request.POST.get('task')
            taskid = request.POST.get('taskid')

            if taskid:
                data = models.TaskModel.objects.filter(id=taskid).first()
                self.form = forms.TaskForm(request.POST,instance=data)
                print('ERRORRR\n\n\n',self.form.errors,'\n\n@@')

            else:

                self.form = self.get_form(forms.TaskForm)
                print('\n\n',self.form,'\n\n@@')
            if self.form.is_valid():

                self.object = self.form.save(commit=False)
                self.object.project_id = id
                self.object.user_id = self.request.user.id
                self.object.save()
                return HttpResponse(id)
            else:
                messages.error(request, "Error")
                print('ERRORRR\n\n\n',self.form.errors,'\n\n@@')
                return HttpResponse('dfgbh')

        else:
            projectid = request.POST.get('projectid')

            if projectid:
                data = models.ProjectModel.objects.filter(id=projectid).first()
                if data:
                    self.form = forms.ProjectForm(request.POST,instance=data)

            else:
                self.form = self.get_form(self.form_class)

            if self.form.is_valid():
                self.object = self.form.save(commit=False)
                self.object.user_id = request.user.id
                self.object.save()
                return redirect('dashboard')

    def delete(self, request, *args, **kwargs):
        put = QueryDict(request.body)
        task_id = put.get('taskid')
        project_id = put.get('projectid')

        if task_id:
            data = models.TaskModel.objects.filter(id=task_id).first()
            if data:
                data.delete()
                return JsonResponse({
                    'status' : 'oke'
                })
            else:
                return JsonResponse({
                    'status': id
                })
        elif project_id:
            data = models.ProjectModel.objects.filter(id=project_id).first()
            if data:
                data.delete()
                return JsonResponse({
                    'status' : 'project'
                })



    def get(self,request,*args,**kwargs):
        # send_mail.delay('nsultanzadeh@gmail.com')
        # print('NARMINNNNN@@@\n\n')
        return super(DashboardView, self).get(request, *args, **kwargs)



class ProjectDetail(generic.DetailView,ModelFormMixin):
    model = models.ProjectModel
    template_name = 'project.html'
    form_class = forms.ProjectForm


    def get_context_data(self, **kwargs):
        self.object = None

        context = super(ProjectDetail, self).get_context_data(**kwargs)
        # context['version'] = ApplicationVersion.objects.all()
        context['task_form'] = forms.TaskForm
        return context

    def post(self,request,*args,**kwargs):
        self.object = None
        id = request.POST.get('taskid')
        project_id = request.POST.get('project')

        status = request.POST.get('status')

        if id:
            data = models.TaskModel.objects.filter(id=id).first()
            if status:
                data.status = status
                data.save()
                return JsonResponse({
                    'status': 'oke'
                })
            else:
                self.form = forms.TaskForm(request.POST, instance=data)
                print('ERRORRR\n\n\n',self.form.errors,'\n\n@@')
        else:
            self.form = self.get_form(forms.TaskForm)
            print('\n\n',self.form,'\n\n@@')

        if self.form.is_valid():

            self.object = self.form.save(commit=False)
            if project_id:
                self.object.project_id = project_id
            self.object.user_id = self.request.user.id
            self.object.save()
            return HttpResponse(id)
        else:
            messages.error(request, "Error")
            print('ERRORRR\n\n\n',self.form.errors,'\n\n@@')
            return HttpResponse('dfgbh')


        #     if taskid:
        #         data = models.TaskModel.objects.filter(id=taskid).first()
        #         self.form = forms.TaskForm(request.POST,instance=data)
        #         print('ERRORRR\n\n\n',self.form.errors,'\n\n@@')
        #
        #     else:
        #
        #         self.form = self.get_form(forms.TaskForm)
        #         print('\n\n',self.form,'\n\n@@')
        #     if self.form.is_valid():
        #
        #         self.object = self.form.save(commit=False)
        #         self.object.project_id = id
        #         self.object.user_id = self.request.user.id
        #         self.object.save()
        #         return HttpResponse(id)
        #     else:
        #         messages.error(request, "Error")
        #         print('ERRORRR\n\n\n',self.form.errors,'\n\n@@')
        #         return HttpResponse('dfgbh')
        #
        # else:
        #     projectid = request.POST.get('projectid')
        #
        #     if projectid:
        #         data = models.ProjectModel.objects.filter(id=projectid).first()
        #         if data:
        #             self.form = forms.ProjectForm(request.POST,instance=data)
        #
        #     else:
        #         self.form = self.get_form(self.form_class)
        #
        #     if self.form.is_valid():
        #         self.object = self.form.save(commit=False)
        #         self.object.user_id = request.user.id
        #         self.object.save()
        #         return redirect('project-detail')

    def delete(self, request, *args, **kwargs):
        put = QueryDict(request.body)
        task_id = put.get('taskid')

        if task_id:
            data = models.TaskModel.objects.filter(id=task_id).first()
            if data:
                data.delete()
                return JsonResponse({
                    'status': 'oke'
                })
            else:
                return JsonResponse({
                    'status': id
                })


class TaskView(generic.ListView):
    template_name = 'task.html'
    model = models.TaskModel

    def get_context_data(self, **kwargs):
        context = super(TaskView, self).get_context_data(**kwargs)
        context['tasks'] = models.TaskModel.objects.filter(user_id=self.request.user.id).order_by('expiration_date')
        context['form'] = forms.TaskForm()
        context['users'] = User.objects.all().exclude(id=self.request.user.id)
        return context

    def post(self, request, *args, **kwargs):
        self.object = None

        if 'task' in request.POST:
            id = request.POST.get('task')
            taskid = request.POST.get('taskid')
            if taskid:
                data = models.TaskModel.objects.filter(id=taskid).first()
                self.form = forms.TaskForm(request.POST, instance=data)
                print('ERRORRR\n\n\n', self.form.errors, '\n\n@@')

            else:

                self.form = self.get_form(forms.TaskForm)
                print('\n\n', self.form, '\n\n@@')
            if self.form.is_valid():

                self.object = self.form.save(commit=False)
                if id:
                    self.object.project_id = id
                self.object.user_id = self.request.user.id
                self.object.save()
                return HttpResponse(id)
            else:
                messages.error(request, "Error")
                print('ERRORRR\n\n\n', self.form.errors, '\n\n@@')
                return HttpResponse('dfgbh')

        else:
            projectid = request.POST.get('projectid')

            if projectid:
                data = models.ProjectModel.objects.filter(id=projectid).first()
                if data:
                    self.form = forms.ProjectForm(request.POST, instance=data)

            else:
                self.form = self.get_form(self.form_class)

            if self.form.is_valid():
                self.object = self.form.save(commit=False)
                self.object.user_id = request.user.id
                self.object.save()
                return redirect('dashboard')

    def delete(self, request, *args, **kwargs):
        put = QueryDict(request.body)
        task_id = put.get('taskid')

        if task_id:
            data = models.TaskModel.objects.filter(id=task_id).first()
            if data:
                data.delete()
                return redirect('tasks')
            else:
                return JsonResponse({
                    'status': id
                })



class TaskFilterView(generic.ListView):
    template_name = 'task.html'
    model = models.TaskModel

    def get_context_data(self, **kwargs):
        name = self.kwargs['name']
        context = super(TaskFilterView, self).get_context_data(**kwargs)
        context['tasks'] = models.TaskModel.objects.filter(type=name).order_by('expiration_date')
        context['form'] = forms.TaskForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        status = request.POST.get('status')

        if status:
            id = request.POST.get('id')
            task = models.TaskModel.objects.filter(id=id).first()
            if task:
                task.status = status
                task.save()

            return JsonResponse({
                'status': 'oke'
            })


        if 'task' in request.POST:
            id = request.POST.get('task')
            taskid = request.POST.get('taskid')
            if taskid:
                data = models.TaskModel.objects.filter(id=taskid).first()
                self.form = forms.TaskForm(request.POST, instance=data)
                print('ERRORRR\n\n\n', self.form.errors, '\n\n@@')

            else:

                self.form = self.get_form(forms.TaskForm)
                print('\n\n', self.form, '\n\n@@')
            if self.form.is_valid():

                self.object = self.form.save(commit=False)
                if id:
                    self.object.project_id = id
                self.object.user_id = self.request.user.id
                self.object.save()
                return HttpResponse(id)
            else:
                messages.error(request, "Error")
                print('ERRORRR\n\n\n', self.form.errors, '\n\n@@')
                return HttpResponse('dfgbh')

        else:
            projectid = request.POST.get('projectid')

            if projectid:
                data = models.ProjectModel.objects.filter(id=projectid).first()
                if data:
                    self.form = forms.ProjectForm(request.POST, instance=data)

            else:
                self.form = self.get_form(self.form_class)

            if self.form.is_valid():
                self.object = self.form.save(commit=False)
                self.object.user_id = request.user.id
                self.object.save()
                return redirect('dashboard')

    def delete(self, request, *args, **kwargs):
        put = QueryDict(request.body)
        task_id = put.get('taskid')

        if task_id:
            data = models.TaskModel.objects.filter(id=task_id).first()
            if data:
                data.delete()
                return redirect('tasks')
            else:
                return JsonResponse({
                    'status': id
                })




class RealtimeIndex(generic.TemplateView):
    template_name = "chat.html"


class RealtimeChat(generic.TemplateView):
    template_name = "mychat.html"


class SharedTask(generic.DetailView):
    model = models.TaskModel
    template_name = 'task-detail.html'

    def get_context_data(self, **kwargs):
        from_name = self.kwargs['from_name']
        to_name = self.kwargs['to_name']
        pk = self.kwargs['pk']
        context = super(SharedTask, self).get_context_data(**kwargs)
        context['task'] = models.TaskModel.objects.filter(id=pk).first()
        # context['form'] = forms.TaskForm()
        context['from_name'] = User.objects.filter(username=from_name).first()
        context['to_name'] = User.objects.filter(username=to_name).first()
        return context