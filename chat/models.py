from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_otp.models import Device
from django_otp.plugins.otp_totp.models import TOTPDevice

class GroupIs(models.Model):
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated', '-created']
        verbose_name = "Group"
        verbose_name_plural = "Groups"
    
    def __str__(self):
        return self.name

class Message(models.Model):
    group = models.ForeignKey(GroupIs, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField() 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated', '-created']
        verbose_name = "Message"
        verbose_name_plural = "Messages"
    
    def __str__(self):
        return f'{self.user.username}:{self.body}'

class MyUser(AbstractUser):
    pass

class OTPDevice(Device):
    pass
