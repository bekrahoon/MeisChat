import json
import logging
from django.template.loader import render_to_string
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Message, GroupIs
from asgiref.sync import sync_to_async


import firebase_admin
from firebase_admin import credentials, messaging

# Инициализация Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate('chat-1a046-firebase-adminsdk-qm11a-66e7a5a6db.json')
    firebase_admin.initialize_app(cred)

async def send_firebase_notification(token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
        webpush=messaging.WebpushConfig(
            notification=messaging.WebpushNotification(
                icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSzJh1CsHFfi4c7ws2wVzarUi_A4CPo-fkCLw&s",
                image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSUQFn0-lTsoToECguElP_8rMAYKnN6Fo5kUA&s"
            )
        )
    )
    response = messaging.send(message)
    return response



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
            self.user = self.scope['user']
            self.group_id = self.scope['url_route']['kwargs']['group_id']
            self.group_name = f'chat_{self.group_id}'
            
            try:
                self.group = await self.get_group(self.group_id)
            except GroupIs.DoesNotExist:
                await self.close()
                return
            
            # Add user to group
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        # Remove user from group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json.get('body', '')
        file_url = text_data_json.get('file_url', '')
        user_token = text_data_json.get('user_token', '')  # Получите токен пользователя для уведомления

        
        if not body and not file_url:
            return
        
        if text_data_json.get('type') == 'file_notification':
            # Обработка уведомления о файле
            file_name = text_data_json.get('file_name')
            user = text_data_json.get('user')
            
            # Генерация HTML для уведомления о файле
            context = {
                'file_name': file_name,
                'user': self.user
            }
            html = await sync_to_async(render_to_string)("base/chat_message_p.html", context=context)
            
            
            # Отправка уведомления в Firebase
            if user_token:
                await send_firebase_notification(
                    token=user_token,
                    title=f"New file from {self.user.username}",
                    body=f"{file_name} has been uploaded."
                )
            
            # Отправка уведомления в группу
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'file_notification',
                    'html': html,
                    'file_name': file_name,
                    'user': self.user.username
                }
            )
        elif text_data_json.get('type') == 'file_uploaded':
            # Обработка загруженного файла
            file_id = text_data_json.get('file_id')
            file_name = text_data_json.get('file_name')
            file_url = text_data_json.get('file_url')
            file_base64 = text_data_json.get('file_base64')
            file_type = text_data_json.get('file_type')
            
            # Генерация HTML для сообщения с файлом
            context = {
                'file_id': file_id,
                'file_name': file_name,
                'file_url': file_url,
                'file_base64': file_base64,
                'file_type': file_type,
                'user': self.user
            }
            html = await sync_to_async(render_to_string)("base/chat_message_p.html", context=context)
            
            # Отправка сообщения в группу
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat_message',
                    'html': html,
                    'file_url': file_url,
                    'user': self.user.username
                }
            )
        else:
            try:
                message = await self.create_message(body, file_url)
            except Exception as e:
                logging.error(f"Error creating message: {e}")
                return

            context = {
                'message': message,
                'user': self.user
            }
            html = await sync_to_async(render_to_string)("base/chat_message_p.html", context=context)

            # Отправка сообщения в группу
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat_message',
                    'html': html,
                    'file_url': file_url,
                    'user': self.user.username
                }
            )

            # Подтверждение доставки сообщения
            await self.send(text_data=json.dumps({
                'type': 'message_delivered',
                'message_id': message.id,
                'status': 'delivered'
            }))
        
            
    
        
    async def chat_message(self, event):
        html = event['html']
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'html': html
        }))
    

    @database_sync_to_async
    def get_group(self, group_id):
        return GroupIs.objects.get(id=group_id)

    @database_sync_to_async
    def create_message(self, body, file_url):
        if file_url:
            return Message.objects.create(body=body, file=file_url, user=self.user, group=self.group)
        else:
            return Message.objects.create(body=body, user=self.user, group=self.group)



    @sync_to_async
    def get_group_participants(self, group):
        return list(group.participants.all())
    
    



