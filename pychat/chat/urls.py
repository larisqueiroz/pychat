from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', EnterChat, name='home'),
    path('<str:chat_name>/<str:username>', SendMessage, name='chat')
]