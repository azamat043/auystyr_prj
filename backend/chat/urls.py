from django.urls import path
from . import views


urlpatterns = [
    path('', views.chat, name='chat'),
    path('get_message_with_user/<int:user_id>/', views.get_message_with_user, name='get_message_with_user'),
    path('send_message_to_user/<int:user_id>/', views.send_message_to_user, name='send_message_to_user'),
]
