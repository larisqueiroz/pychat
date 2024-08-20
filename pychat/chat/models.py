import uuid
from django.db import models

class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Chat(Base):
    name = models.CharField(null=False, blank=False, max_length= 50, unique=True)
    final_datetime = models.DateTimeField(null=True, blank=True)
    initial_datetime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class User(Base):
    username = models.CharField(max_length=15, null=False, blank=False, unique=True)
    """password = models.CharField(max_length=12, null=False, blank=False)
    email = models.CharField(max_length=50, null=False, blank=False)"""

class Message(Base):
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE)
    content = models.CharField(null=True, max_length=1000, blank=True)
    img_base64 = models.ImageField(null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime_sent = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self):
        return self.content
