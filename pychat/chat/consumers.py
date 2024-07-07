from channels.generic.websocket import AsyncWebsocketConsumer


class Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_name = f"chat_{self.scope['url_route']['kwargs']['chat_name']}"
        await self.channel_layer.group_add(self.chat_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.chat_name, self.channel_name)
