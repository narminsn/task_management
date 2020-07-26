from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions
from .forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth.views import LoginView

class ObtainTokenPairWithColorView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    # print('narminnnnnnnn\n\n\n',response.data.access,'\n\n')


class MySignUpView(View):
    form_class = UserCreationForm
    template_name = 'user/auth_register_boxed.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            u = User.objects.create_user(
                form.cleaned_data.get('username'),
                form.cleaned_data.get('email'),
                form.cleaned_data.get('password1'),
                is_active=True
            )
            # TODO Display message and redirect to login
            return HttpResponseRedirect('/accounts/login/?next=/')
        # return render(request, self.template_name, {'form': form})r-login.html')


