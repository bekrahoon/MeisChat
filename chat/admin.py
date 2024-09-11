from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import *




@admin.register(GroupIs)
class GroupIsAdmin(ModelAdmin):
    list_display = ('name', 'host', 'updated', 'created')
    list_filter = ('updated', 'created')
    search_fields = ('name', 'description')
    
    
    
    

@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ('group', 'user', 'body', 'read', 'updated', 'created')
    list_filter = ('created', 'group')
    search_fields = ('body', 'user__username', 'group__name')



@admin.register(MyUser)
class MyUserAdmin(ModelAdmin):
    list_display = ('username','email', 'phone_number', 'is_active', 'is_suspended')
    list_filter = ('is_active', 'is_suspended')
    search_fields = ('username', 'email')
    
    actions = ['ban_user', 'suspend_user', 'activate_user']
    
    def ban_user(self, request, queryset):
        queryset.update(is_active=False)
    ban_user.short_description = "Заблокировать выбранных пользователей"

    def suspend_user(self, request, queryset):
        queryset.update(is_suspended=True)
    suspend_user.short_description = "Приостановить выбранные аккаунты"

    def activate_user(self, request, queryset):
        queryset.update(is_active=True, is_suspended=False)
    activate_user.short_description = "Активировать выбранные аккаунты"







@admin.register(OTPDevice)
class OTPDeviceAdmin(ModelAdmin):
    list_display = ('otp', 'created_at')


@admin.register(UserStatus)
class UserStatusAdmin(ModelAdmin):
    list_display = ('user', 'status')


