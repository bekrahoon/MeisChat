import json
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime
from django.utils.timesince import timesince

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.group_name = f'chat_{self.group_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_body = text_data_json['message']
        user = self.scope['user']
        created = datetime.now().isoformat()  # or use another format

        # Send message to room group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': message_body,
                'user': user.username,
                'created': created,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        created = event['created']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'created': created,
        }))


# consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer

class OnlineTrackerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'online_users'
        
        # Добавление пользователя в группу
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        # Сообщение о присоединении пользователя
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'user_status',
                'message': f'<span style="color: green">{self.scope["user"].username} is online</span>',
                'user_id': self.scope["user"].id,
                'status': 'online'
            }
        )

    async def disconnect(self, close_code):
        # Сообщение об отключении пользователя
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'user_status',
                'message': f'<span style="color: red">{self.scope["user"].username} is offline</span>',
                'user_id': self.scope["user"].id,
                'status': 'offline'
            }
        )

        # Удаление пользователя из группы
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Обработка входящих сообщений (если необходимо)
        pass

    async def user_status(self, event):
        message = event['message']
        user_id = event['user_id']
        status = event['status']

        # Отправка сообщения WebSocket клиенту
        await self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id,
            'status': status
        }))