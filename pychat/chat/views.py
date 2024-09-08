import jwt
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from rest_framework.authentication import CSRFCheck, SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.utils import json
from rest_framework import exceptions
from django.middleware.csrf import get_token
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework.views import APIView
import requests

from .models import *
from django.conf import settings

from .serializers import UserSerializer
from .utils import generate_token, generate_refresh_token

@permission_classes([IsAuthenticated])
def EnterChat(request, username):
    jwt_token = request.COOKIES.get('jwt')
    refresh_token = request.COOKIES.get('refreshtoken')

    if not jwt_token:
        return HttpResponseBadRequest("Unauthenticated.")

    try:
        access_token = jwt_token
        payload = jwt.decode(
            access_token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        try:
            refresh = jwt.decode(
                refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            redirect('signin')
    except (jwt.InvalidTokenError, jwt.DecodeError):
        return HttpResponseBadRequest("Invalid token")

    if request.method == 'POST':
        chat_name = request.POST['chat_name']
        print(username, chat_name)

        saved_user = User.objects.filter(username=username)
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
            return redirect('chat', chat_name=chat_name, username=username)
    return render(request, 'lobby.html')

@permission_classes([IsAuthenticated])
def ReadAndSendMessage(request, chat_name, username):
    jwt_token = request.COOKIES.get('jwt')
    refresh_token = request.COOKIES.get('refreshtoken')
    if not jwt_token:
        return HttpResponseBadRequest("Unauthenticated.")

    try:
        access_token = jwt_token
        payload = jwt.decode(
            access_token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        try:
            refresh = jwt.decode(
                refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            redirect('signin')
    except (jwt.InvalidTokenError, jwt.DecodeError):
        return HttpResponseBadRequest("Invalid token")

    chat = Chat.objects.filter(active=True).get(name=chat_name)
    messages = Message.objects.filter(active=True).filter(chat_id=chat.id)

    context = {
        "messages": messages,
        "user": username,
        "chat_name": chat_name,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    print(context)
    return render(request, 'chat.html', context)

def SignUp(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if username == "" or password == "":
            return HttpResponseBadRequest("Username and password are required")

        exists = User.objects.get(username=username).first()
        if exists is not None:
            return HttpResponseBadRequest(f"Username not available.")

        try:
            user = User(username=username, password=make_password(password))
            user.save()
            return redirect('signin')
        except Exception as e:
            return HttpResponseBadRequest(f"Error while saving: {str(e)}")

    return render(request, 'signup.html')

@permission_classes([AllowAny])
def SignIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if username == "" or password == "":
            return HttpResponseBadRequest("Username and password are required.")

        exists = User.objects.filter(username=username).first()
        if exists is None:
            return HttpResponseNotFound(f"User not found.")
        if not exists.check_password(password):
            return HttpResponseBadRequest("Wrong password.")

        token = generate_token(exists)
        refresh_token = generate_refresh_token(exists)

        response = HttpResponseRedirect('/' + str(username) + '/')
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
        response.headers["Authorization"] = "Bearer " + str(token)

        print(refresh_token)
        print(token)

        return response
    return render(request, 'login.html')

def SignOut(request):
    response = HttpResponseRedirect('signin')
    response.delete_cookie('jwt')
    response.delete_cookie('refreshtoken')
    return response