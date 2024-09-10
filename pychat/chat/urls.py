from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('<str:username>/', EnterChat, name='lobby'),
    path('<str:chat_name>/<str:username>', ReadAndSendMessage, name='chat'),
    path('signup', SignUp, name='signup'),
    path('signin', SignIn, name='signin'),
    path('signout', SignOut, name='signout'),
]