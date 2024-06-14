from django.db.models import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from rest_framework.utils import json

from .models import *

def EnterChat(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        
        username = body['username']
        chat_name = body['chat_name']

        saved_user = User.objects.filter(username=username) # TODO deixar o username unico
        saved = list(saved_user)
        if saved == []:
            new_user = User(username=username)
            new_user.save()

        try:
            saved = Chat.objects.get(name=chat_name)
            return redirect('chat', chat_name=chat_name, username=username)
        except:
            new_chat = Chat(name=chat_name)
            new_chat.save()
    return render(request, 'lobby.html')

def SendMessage(request):
    return render(request, 'chat.html')