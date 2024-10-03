from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django_otp.models import Device
from cryptography.fernet import Fernet, InvalidToken
from decouple import config
from typing import Optional
import logging

User = settings.AUTH_USER_MODEL

# Инициализация Fernet для шифрования
ENCRYPT_KEY = config("ENCRYPT_KEY")
f = Fernet(ENCRYPT_KEY)


class GroupIs(models.Model):
    host: Optional[User] = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name: str = models.CharField(max_length=200)
    description: Optional[str] = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    members = models.ManyToManyField(User, related_name="chat_groups", blank=True)
    is_private: bool = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "-created"]
        verbose_name = "Group"
        verbose_name_plural = "Groups"

    def __str__(self) -> str:
        return self.name


class Message(models.Model):
    group: GroupIs = models.ForeignKey(
        GroupIs, related_name="chat_messages", on_delete=models.CASCADE
    )
    user: User = models.ForeignKey(User, on_delete=models.CASCADE)
    body: Optional[str] = models.TextField(max_length=1024, blank=True, null=True)
    file: Optional[models.FileField] = models.FileField(
        upload_to="files/", blank=True, null=True
    )
    read: bool = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def body_decrypted(self) -> str:
        if self.body:
            try:
                # Преобразуем строку в байты перед расшифровкой
                message_decrypted: str = f.decrypt(self.body.encode("utf-8")).decode(
                    "utf-8"
                )
                return message_decrypted
            except (InvalidToken, AttributeError) as e:
                logging.error(f"Ошибка расшифровки сообщения {self.id}: {e}")
                return "Ошибка расшифровки сообщения"
        return ""

    class Meta:
        ordering = ["-updated", "-created"]
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self) -> str:
        return f'{self.user.username}:{self.body if self.body else "Media Message"}'


class MyUser(AbstractUser):
    phone_number: Optional[str] = models.CharField(max_length=15, blank=True, null=True)
    is_suspended: bool = models.BooleanField(default=False)
    fcm_token: Optional[str] = models.CharField(max_length=255, blank=True, null=True)


class OTPDevice(Device):
    otp: str = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)


class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status: str = models.CharField(max_length=10, default="offline")

    def __str__(self) -> str:
        return f"{self.user.username}: {self.status}"
