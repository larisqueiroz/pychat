import datetime

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from .models import Chat, Message, User


class Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_name = f"{self.scope['url_route']['kwargs']['chat_name']}"
        self.group_name = f'chat_{self.chat_name}'
        await self.channel_layer.group_add(self.chat_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.chat_name, self.channel_name)

    async def receive(self, text_data):
        text_json = json.loads(text_data)
        message = text_json

        event = {
            'type': 'send_message',
            'message': message,
        }
        await self.channel_layer.group_send(self.chat_name, event)

    async def send_message(self, event):
        data = event['message']
        await self.create(data=data)
        response = {
            'sender': data['sender'],
            'message': data['message'],
            'datetime_sent': data['datetime_sent'],
            'image_base64': data['image_base64']
        }
        await self.send(text_data=json.dumps({'message': response}))

    @database_sync_to_async
    def create(self, data):
        print(data)
        chat_by_name = Chat.objects.get(name=data['chat_name'])
        sender = User.objects.get(username=data['sender'])
        if not Message.objects.filter(user_id=sender.id).filter(chat_id=chat_by_name.id)\
                .filter(content=data['message']).exists():
            new_message = Message(chat_id=chat_by_name, datetime_sent= data['datetime_sent'],
                                  user_id=sender, content=data['message'], img_base64=data['image_base64'])
            new_message.save()