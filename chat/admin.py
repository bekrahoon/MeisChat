from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(GroupIs)
admin.site.register(OTPDevice)
admin.site.register(Message)
admin.site.register(MyUser)

