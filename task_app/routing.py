from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('comment/<str:room_name>', consumers.ChatConsumer),
    path('chat/<str:room_name>', consumers.MyConsumer),
    path('notification/<int:from_user>', consumers.NotificationConsumer),
    path('comments/<int:from_user>/<int:to_user>/<int:task_id>', consumers.CommentConsumer),

]
