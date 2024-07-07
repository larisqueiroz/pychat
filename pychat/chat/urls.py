from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', EnterChat, name='lobby'),
    path('<str:chat_name>/<str:username>', ReadAndSendMessage, name='chat')
]