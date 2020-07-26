from django import forms
from django.contrib.auth import get_user_model
# from .models import Register
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
User = get_user_model()



class UserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("Sifreler bir birleriyle uygunlasmadi."),
        "is_active": _("Active user oldugunu qeyd edin."),
}

    password1 = forms.CharField(label=_("Password"),
                                    widget=forms.PasswordInput,
                            error_messages={
                                    "required": "Bu xana doldurulmalidir"})

    password2 = forms.CharField(label=_("Password confirmation"),
                                    widget=forms.PasswordInput,
                                    help_text=_("Enter the same password as above, for verification."),
                                    error_messages = {
                                    "required": "Bu xana doldurulmalidir"})




    class Meta:
        model = User
        fields = (

                  "username",
                  "email",
                  "password1",
                  "password2")



        error_messages = {

            "email": {
                "invalid": "Email duzgun qeyd olunamyib",
                "required": "Duzgun daxil edilmeyib",
            },
            "first_name": {
                "invalid": "Adiniz qeyd edin",
                "required": "Duzgun daxil edilmeyib",
            },
            "password1": {
                "required": "Bu xana doldurulmalidir",
                "invalid": "Duzgun qeyd edin sifrenizi",
            },
            "password2": {
                "required": "Bu xana doldurulmalidir",
                "invalid": "Duzgun qeyd edin sifrenizi",
            }
        },

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2



    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class MyUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=_("Password"),
                                         help_text=_(
                                             "Raw şifrələr bazada saxlanmır, onları heç cürə görmək mümkün deyil "
                                             "bu istifadəçinin şifrəsidir, lakin siz onu dəyişə bilərsiziniz "
                                             " <a href=\"../password/\">bu form</a>. vasitəsilə"))
    '''
    burda all cixarmatga ehtiyac yoxdur mence, deyismek olar mence
    '''

    class Meta:
        model = User
        fields = (
         "first_name",
         "last_name",
         "email",
         "is_staff",
         "is_active",)
        # exclude = ("is_superuser",)
        # error_messages = {
        #     "date_joined": {
        #         "required": "Bu xana doldurulmalidir",
        #         "invalid": "Duzgun daxil edilmeyib",

    def __init__(self, *args, **kwargs):
        super(MyUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        # self.fields['date_joined'].required = False
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())

    password = forms.CharField(widget=forms.PasswordInput())