from django.urls import path
from . import  views

urlpatterns = [
    path('dashboard/',views.DashboardView.as_view(),name='dashboard' ),
    path('projects/<int:pk>/', views.ProjectDetail.as_view(),name='project-detail'),
    path('tasks/',views.TaskView.as_view(),name='tasks'),
    path('tasks/<str:name>', views.TaskFilterView.as_view(), name='tasksfilter'),
    path('chat/', views.RealtimeIndex.as_view(), name="main"),
    path('mychat/', views.RealtimeChat.as_view(), name="my-chat"),
    path('task/<int:pk>/<str:from_name>/<str:to_name>', views.SharedTask.as_view(), name="shared-task"),

]
