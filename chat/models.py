from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_otp.models import Device
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.models import Device
from django.utils import timezone
from datetime import timedelta


class GroupIs(models.Model):
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='participants', blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name= 'chat_groups', blank=True)
    is_private = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ['-updated', '-created']
        verbose_name = "Group"
        verbose_name_plural = "Groups"
    
    def __str__(self):
        return self.name

class Message(models.Model):
    group = models.ForeignKey(GroupIs,related_name="chat_messages", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField() 
    file = models.FileField(upload_to='files/', blank=True, null=True)  
    read = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated', '-created']
        verbose_name = "Message"
        verbose_name_plural = "Messages"
    
    def __str__(self):
        return f'{self.user.username}:{self.body if self.body else "Media Message"}'

class MyUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_suspended = models.BooleanField(default=False)
    fcm_token = models.CharField(max_length=255, blank=True, null=True)
    


class OTPDevice(Device):
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # OTP действителен в течение 10 минут
        return timezone.now() < self.created_at + timedelta(minutes=10)

# models.py

from django.db import models

class UserStatus(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default='offline')

    def __str__(self):
        return f"{self.user.username}: {self.status}"



#       source newenv/Scripts/activate
#       py manage.py runserver
#       py manage.py makemigrations
#       py manage.py migrate
