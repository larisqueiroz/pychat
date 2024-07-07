from .consumers import Consumer
from django.urls import path

websockets_urlpatterns = [
    path('ws/notification/<str:chat_name>/', Consumer.as_asgi())
]