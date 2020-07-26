from django.urls import path
from .views import ObtainTokenPairWithColorView
from . import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('api/token/', ObtainTokenPairWithColorView.as_view(), name='token_obtain_pair'),
    path('register/',views.MySignUpView.as_view(),name='register'),
    path('login/', LoginView.as_view(), name='login'),

    # path('current_user/', current_user),
    # path('users/', UserList.as_view())
]