from django.contrib import admin
from unfold.admin import ModelAdminMixin
from .models import GroupIs, Message, MyUser, OTPDevice, UserStatus

class GroupIsAdmin(ModelAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'host', 'updated', 'created')

class MessageAdmin(ModelAdminMixin, admin.ModelAdmin):
    list_display = ('group', 'user', 'body', 'read', 'updated', 'created')

class MyUserAdmin(ModelAdminMixin, admin.ModelAdmin):
    list_display = ('username', 'phone_number')

class OTPDeviceAdmin(ModelAdminMixin, admin.ModelAdmin):
    list_display = ('otp', 'created_at')

class UserStatusAdmin(ModelAdminMixin, admin.ModelAdmin):
    list_display = ('user', 'status')

admin.site.register(GroupIs, GroupIsAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(MyUser, MyUserAdmin)
admin.site.register(OTPDevice, OTPDeviceAdmin)
admin.site.register(UserStatus, UserStatusAdmin)

