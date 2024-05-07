import uuid
from django.db import models

class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Chat(Base):
    final_datetime = models.DateTimeField(null=True, blank=True)
    initial_datetime = models.DateTimeField(null=True, blank=True)

class User(Base):
    chat = models.ForeignKey(Chat, on_delete=models.DO_NOTHING)
    username = models.CharField(max_length=15, null=False, blank=False)
    password = models.CharField(max_length=12, null=False, blank=False)
    email = models.CharField(max_length=50, null=False, blank=False)

class Message(Base):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    content = models.CharField(null=False, max_length=500, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime_sent = models.DateTimeField(null=True, blank=True, default=None)
