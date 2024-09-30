from django.template.loader import render_to_string
from .models import Message, GroupIs, MyUser
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from firebase_admin import credentials, messaging
from asgiref.sync import sync_to_async
from cryptography.fernet import Fernet
from decouple import config
import firebase_admin
import logging
import json


# Инициализация Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(config("FIREBASE_SERVICE_ACCOUNT_KEY"))
    firebase_admin.initialize_app(cred)

# Инициализация Fernet для шифрования
ENCRYPT_KEY = config('ENCRYPT_KEY')
f = Fernet(ENCRYPT_KEY)


async def send_firebase_notification(token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
        webpush=messaging.WebpushConfig(
            notification=messaging.WebpushNotification(
                icon="static/images/3062634.png",
                image="static/images/3062634.png",
            )
        ),
    )
    response = messaging.send(message)
    return response


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        
        # Убедитесь, что self.user - это экземпляр кастомного пользователя
        if not isinstance(self.user, MyUser):
            await self.close()
            return
        
        self.group_id = self.scope["url_route"]["kwargs"]["group_id"]
        self.group_name = f"chat_{self.group_id}"

        try:
            self.group = await self.get_group(self.group_id)
        except GroupIs.DoesNotExist:
            await self.close()
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json.get("body", "")
        file_url = text_data_json.get("file_url", "")
        file_name = text_data_json.get("file_name", "")
        user_token = text_data_json.get("user_token", "")

        if not body and not file_url:
            return

        if text_data_json.get("type") == "file_uploaded":
            # Генерация HTML для сообщения с файлом
            context = {"file_name": file_name, "file_url": file_url, "user": self.user}
            html = await sync_to_async(render_to_string)(
                "base/chat_message_p.html", context=context
            )

            # Отправка сообщения в группу
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chat_message",
                    "html": html,
                    "file_url": file_url,
                    "user": self.user.username,
                    "file_name": file_name,  # Передаем имя файла
                },
            )
        else:
            try:
                # Шифрование сообщения перед сохранением
                encrypted_body = f.encrypt(body.encode("utf-8")).decode("utf-8")

                message = await self.create_message(encrypted_body, file_url)

                context = {"message": message, "user": self.user}

                # Генерация HTML для сообщения
                html = await sync_to_async(render_to_string)(
                    "base/chat_message_p.html", context=context
                )

                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "chat_message",
                        "html": html,
                        "file_url": file_url,
                        "user": self.user.username,
                        "message_id": message.id,  # Передаем ID сообщения для расшифровки
                    },
                )

                await self.send(
                    text_data=json.dumps(
                        {
                            "type": "message_delivered",
                            "message_id": message.id,
                            "status": "delivered",
                        }
                    )
                )

            except Exception as e:
                logging.error(f"Error creating message: {e}")

    async def chat_message(self, event):
        html = event["html"]

        # Расшифровка сообщения перед отправкой клиенту (если нужно)
        try:
            message_id = event.get("message_id")
            if message_id:
                message = await self.get_message(message_id)
                decrypted_body = f.decrypt(message.body.encode("utf-8")).decode("utf-8")
            else:
                decrypted_body = "Сообщение не найдено"

            await self.send(
                text_data=json.dumps(
                    {
                        "type": "chat_message",
                        "html": html,
                        "body": decrypted_body,  # Отправляем расшифрованное сообщение клиенту
                    }
                )
            )
        except Exception as e:
            logging.error(f"Error decrypting message: {e}")
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "chat_message",
                        "html": html,
                        "body": "Ошибка расшифровки сообщения",
                    }
                )
            )

    @database_sync_to_async
    def get_group(self, group_id):
        return GroupIs.objects.get(id=group_id)

    @database_sync_to_async
    def create_message(self, body, file_url):
        if file_url:
            return Message.objects.create(
                body=body, file=file_url, user=self.user, group=self.group
            )
        else:
            return Message.objects.create(body=body, user=self.user, group=self.group)

    @database_sync_to_async
    def get_message(self, message_id):
        return Message.objects.get(id=message_id)
