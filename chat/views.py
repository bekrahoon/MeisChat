import os
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer
from asgiref.sync import  async_to_sync
from django.urls import reverse
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
# from .tasks import mark_message_as_received
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.core.mail import send_mail
from twilio.rest import Client
from django.conf import settings
import random
from django.dispatch import receiver
from django.http import HttpResponseForbidden
from .decorators import suspended_decorator
import requests
from functools import wraps
import json
import requests
from google.oauth2 import service_account
import google.auth.transport.requests
import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import IntegrityError

from cryptography.fernet import Fernet

# f = Fernet(settings.ENCRYPT_KEY)
    
def generate_otp():
    return random.randint(100000, 999999)

def send_otp_via_email(email, otp):
    logger.debug(f"Sending OTP {otp} to email {email}")
    subject = 'Your OTP Code'
    message = f'Your OTP is {otp}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

def send_otp_via_sms(phone_number, otp):
    logger.debug(f"Sending OTP {otp} to phone number {phone_number}")
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f'Your OTP is {otp}',
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return message.sid


def loginPage(request):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            otp = generate_otp()
            request.session['otp'] = otp

            # Отправка OTP пользователю
            if user.phone_number:
                send_otp_via_sms(user.phone_number, otp)
                messages.success(request, 'OTP sent to your phone.')
            elif user.email:
                send_otp_via_email(user.email, otp)
                messages.success(request, 'OTP sent to your email.')
            else:
                messages.error(request, 'No contact information associated with this account.')

            request.session['otp_user_id'] = user.id
            
            return redirect('verify_otp')
        else:
            messages.error(request, 'Invalid login credentials.')
    else:
        form = CustomAuthenticationForm()
    
    context = {'page': page, 'form': form}
    return render(request, 'base/login.html', context)



def change_login(request):
    # Очистка сессии для удаления OTP информации
    request.session.pop('otp_user_id', None)
    
    # Перенаправление на страницу входа
    return redirect('login')


import logging
from django.contrib.auth import login

logger = logging.getLogger(__name__)

def verify_otp(request):
    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        user_id = request.session.get('otp_user_id')
        session_otp = request.session.get('otp')

        logger.debug(f"User ID: {user_id}, Input OTP: {otp_input}, Session OTP: {session_otp}")

        if not user_id:
            messages.error(request, 'User session not found')
            return redirect('login')

        user = get_object_or_404(MyUser, id=user_id)

        # Преобразуйте значения в строки перед сравнением
        if session_otp and str(otp_input).strip() == str(session_otp).strip():
            login(request, user)
            request.session.pop('otp_user_id', None)
            request.session.pop('otp', None)
            messages.success(request, 'Successfully logged in')
            return redirect('home')
        else:
            logger.error("Invalid OTP Error")
            messages.error(request, 'Invalid OTP')
            return redirect('verify_otp')

    user_id = request.session.get('otp_user_id')
    user = get_object_or_404(MyUser, id=user_id) if user_id else None
    context = {'user': user}
    return render(request, 'base/login.html', context)


def resend_otp(request):
    user_id = request.session.get('otp_user_id')
    if not user_id:
        messages.error(request, 'User session not found')
        return redirect('login')

    user = get_object_or_404(MyUser, id=user_id)
    otp = generate_otp()  # Генерируем новый OTP
    
    # Преобразуйте OTP в строку перед сохранением в сессии
    request.session['otp'] = str(otp)

    if user.phone_number:
        send_otp_via_sms(user.phone_number, otp)
    elif user.email:
        send_otp_via_email(user.email, otp)
    else:
        messages.error(request, 'No contact information associated with this account.')
        return redirect('verify_otp')

    logger.debug(f"New OTP: {otp} saved in session")
    messages.success(request, 'OTP has been resent to your email or phone.')
    return redirect('verify_otp')




def suspended_view(request):
    return render(request, 'base/suspended.html', {
        'message': "Ваш аккаунт был приостановлен. Свяжитесь с поддержкой для получения информации."
    })





def registerPage(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = MyUserCreationForm()

    context = {'form': form}
    return render(request, 'base/register.html', context)



def logoutUser(request):
    logout(request)
    return redirect('home')






@login_required
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    q = request.GET.get('q') if request.GET.get('q') else ''
    
    # Поиск по группам
    groups = GroupIs.objects.filter(
    Q(name__icontains=q) | Q(description__icontains=q),
    Q(participants__id=request.user.id) | Q(host=request.user)
).distinct()
    
    
    group_count = groups.count()

    # Поиск по сообщениям
    group_messages = Message.objects.filter(
        Q(group__name__icontains=q)
    )

    # Поиск по пользователям
    users = MyUser.objects.filter(
        Q(username__icontains=q) |
        Q(email__icontains=q)
    )

    
    context = {
        'groups': groups, 
        'group_count': group_count, 
        'group_messages': group_messages,
        'users': users,  
        'q': q  # Передача строки поиска в контекст для отображения в шаблоне
    }
    
    return render(request, 'base/home.html', context)



@suspended_decorator
@login_required
def group(request, pk):    
    
    if request.user.is_authenticated !=  True:
        return redirect('login')
    
    page = 'participants'
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    groups = GroupIs.objects.filter(
    Q(name__icontains=q) | Q(description__icontains=q),
    Q(participants__id=request.user.id) | Q(host=request.user)
).distinct()
    
    group_count = groups.count()
    group_messages = Message.objects.filter(
        Q(group__name__icontains = q)
        )
    users = MyUser.objects.filter(
        Q(username__icontains=q) |
        Q(email__icontains=q)
    )
    
    
    group = GroupIs.objects.get(id=pk)
    group_messages = group.chat_messages.order_by('-created')
    participants = group.participants.all()
    if request.user.is_suspended:
        return HttpResponseForbidden("Ваш аккаунт приостановлен.")
    
    other_user  = None
    if group.is_private:
        if  request.user not in group.members.all():
            raise Http404()
        for  member in group.members.all():
            if member != request.user:
                other_user = member
                break
            
    
    
    form = MessageCreationForm()
    
    if request.htmx:
        form = MessageCreationForm(request.POST)
        if form.is_valid:
            message = form.save(commit=False)

                    
            message.user = request.user
            message.group = group
            message.save()
            context = {
                'message':message,
                'user':request.user
            }
            
            return render(request, 'base/chat_message_p.html', context)

        


    context = {'group':group, 'group_messages':group_messages,
               'participants':participants,
               'groups':groups, 
               'group_count':group_count, 
               'page':page,
               'form':form,
               'other_user':other_user,
               'users':users,
               'pk':pk}
    
    return render(request, 'base/group.html', context)

@login_required
def get_or_create_chat(request, pk):
    if request.user.id == pk:
        return redirect('home')
    
    other_user = MyUser.objects.get(pk=pk)
    
    # Поиск существующего чата
    chat = GroupIs.objects.filter(
        is_private=True,
        members=other_user
    ).filter(
        members=request.user
    ).first()  # Получаем первый подходящий чат, если он есть
    
    # Если чат не найден, создаем новый
    if chat is None:
        chat = GroupIs.objects.create(is_private=True)
        chat.members.add(other_user, request.user)
    
    return redirect('group', chat.id)





@login_required
def update_message_status(request, message_id):
    if request.method == 'POST':
        try:
            message = Message.objects.get(id=message_id)
            message.read = True
            message.save()
            return JsonResponse({'status': 'success'})
        except Message.DoesNotExist:
            return JsonResponse({'error': 'Message not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)







def chat_file_upload(request, pk):
    if request.method == 'POST' and request.FILES:
        try:
            file = request.FILES['file']
            file_name = file.name

            # Создаем новое сообщение с файлом
            message = Message.objects.create(
                file=file,
                user=request.user,
                group_id=pk,
            )

            # Проверяем, был ли файл успешно загружен
            if message.file:
                # Отправка уведомления через WebSocket
                channel_layer = get_channel_layer()
                event = {
                    'type': 'chat_file',
                    'file_url': message.file.url,
                    'file_name': file_name,
                    'user': request.user.username
                }
                async_to_sync(channel_layer.group_send)(
                    f"group_{pk}",
                    event
                )
                return JsonResponse({'file_url': message.file.url, 'file_name': file_name})
            else:
                return JsonResponse({'error': 'Файл не был загружен'}, status=400)
        except Exception as e:
            # Логирование исключения и возврат ошибки
            print(f"Error in file upload: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method or no file uploaded'}, status=400)






def participants(request, pk):    
    
    if request.user.is_authenticated !=  True:
        return redirect('login')
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    groups = GroupIs.objects.filter(
    Q(name__icontains=q) | Q(description__icontains=q),
    Q(participants__id=request.user.id) | Q(host=request.user)
).distinct()
    
    group_count = groups.count()
    group_messages = Message.objects.filter(
        Q(group__name__icontains = q)
        )
    group = GroupIs.objects.get(id=pk)
    group_messages = group.chat_messages.order_by('-created')
    participants = group.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            group=group,
            body=request.POST.get('body')
        )
        if message:
            print("Сообщение успешно сохранено:", message.body)
        else:
            print("Ошибка при сохранении сообщения")
        group.participants.add(request.user)
        return redirect('group', pk=group.id)


    context = {'group':group, 'group_messages':group_messages,
               'participants':participants,
               'groups':groups, 
               'group_count':group_count, 
               'group_messages':group_messages,
               }
    
    return render(request, 'base/participants.html', context)




def group_view(request, pk):
    group = GroupIs.objects.get(pk=pk)
    messages = Message.objects.filter(group=group).order_by('created')
    context = {'group': group, 'messages': messages}
    
    return render(request, 'base/group.html', context) 





def userProfile(request, pk):
    user = get_object_or_404(MyUser, id=pk)
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            form = MyUserCreationForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('user_profile', pk=user.id)
        elif 'send_sms' in request.POST:
            otp = generate_otp()  # Генерация OTP, добавьте эту функцию, если она не определена
            if user.phone_number:
                send_otp_via_sms(user.phone_number, otp)
                messages.success(request, 'SMS sent successfully!')
            else:
                messages.error(request, 'No phone number associated with this account.')
            return redirect('user_profile', pk=user.id)
    else:
        form = MyUserCreationForm(instance=user)
    
    groups = user.groupis_set.all()
    group_messages = user.message_set.order_by('-created')
    
    context = {
        'user': user,
        'groups': groups,
        'group_messages': group_messages,
        'form': form
    }
    return render(request, 'base/profile.html', context)



@login_required
def profile_update(request, pk):
    user = get_object_or_404(MyUser, id=pk)
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('user_profile', pk=user.pk)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ProfileUpdateForm(instance=user)
    
    context = {
        'user': user,
        'form': form,
    }
    
    return render(request, 'base/profile.html', context)



@login_required(login_url = 'login')
def createGroup(request):
    form = GroupIsForm()
    if request.method == 'POST':
        form = GroupIsForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.host = request.user
            group.save()
            return redirect('home')
            
            
            
    context = {'form':form}
    return render(request,  'base/group_form.html', context)



@login_required(login_url = 'login')
def updateGroup(request, pk):
    group  =  GroupIs.objects.get(id=pk)
    form = GroupIsForm(instance=group)
    
    if request.user != group.host:
        return HttpResponse('You are not allowed here!!')
    
    if request.method == 'POST':
        form = GroupIsForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    
    
    context = {'form':form}
    
    return render(request, 'base/group_form.html', context)



@login_required(login_url = 'login')
def deleteGroup(request, pk):
    group = GroupIs.objects.get(id=pk)
    if request.user != group.host:
        return HttpResponse('You are not allowed here!!')
    
    if request.method == 'POST':
        group.delete() 
        return redirect('home')
    return render(request, "base/delete.html", {'obj':group})


from django.http import HttpResponseRedirect

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')
    
    if request.method == 'POST':
        message.delete()
        
        # Получаем URL для редиректа из формы (или перенаправляем на главную, если его нет)
        next_url = request.POST.get('next', 'home')
        return redirect(next_url)
    
    # Передаём реферер в форму для дальнейшего использования
    return render(request, "base/delete.html", {'obj': message, 'next': request.META.get('HTTP_REFERER', 'home')})









def save_fcm_token(request):
    if request.method == 'POST':
        token = request.POST.get('fcm_token')
        print(f"Received token: {token}")  # Логирование для отладки
        if not token:
            return JsonResponse({'status': 'error', 'message': 'Token not provided'}, status=400)
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=401)
        
        user = get_object_or_404(MyUser, id=request.user.id)
        
        user.fcm_token = token
        user.save()
        print(f"Token saved for user: {user.username}")
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)




# Путь к вашему файлу сервисного аккаунта
SERVICE_ACCOUNT_FILE = 'chat-1a046-firebase-adminsdk-qm11a-66e7a5a6db.json'

# Аутентификация с использованием сервисного аккаунта
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/firebase.messaging'])
request = google.auth.transport.requests.Request()
scoped_credentials.refresh(request)

access_token = scoped_credentials.token  # Токен доступа



def send_notification(token, title, body, click_action_url=None):
    url = "https://fcm.googleapis.com/v1/projects/chat-1a046/messages:send"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    message = {
        "token": token,
        "notification": {
            "title": title,
            "body": body
        },
        "webpush": {
            "notification": {
                "icon": "https://cdn-icons-png.flaticon.com/512/5356/5356355.png",
                "image": "https://img.freepik.com/free-photo/reminder-popup-bell-notification-alert-or-alarm-icon-sign-or-symbol-for-application-website-ui-on-purple-background-3d-rendering-illustration_56104-1304.jpg",
                "click_action": click_action_url or "https://your-default-url.com"
            }
        }
    }

    payload = {
        "message": message
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Notification sent successfully:", response.json())
    else:
        # Логируем ошибку и удаляем невалидный токен
        print("Failed to send notification:", response.status_code, response.json())
        if response.status_code == 404:
            # Пример кода для удаления невалидного токена
            try:
                MyUser.objects.filter(fcm_token=token).update(fcm_token=None)
            except IntegrityError as e:
                print("Error updating token:", e)

                
                
@receiver(post_save, sender=Message)
def notify_users(sender, instance, created, **kwargs):
    if created:
        group = instance.group
        
        # Проверка, является ли группа публичной или личной
        if group.is_private:  # Предположим, что у группы есть флаг is_private
            users = group.members.all()  # Личные переписки
        else:
            users = group.participants.all()  # Публичные группы
            
        user_tokens = users.values_list('fcm_token', flat=True)  # Преобразование QuerySet в список

        for token in set(user_tokens):
            if token:
                # Формирование URL с идентификатором группы
                message_url = f"http://127.0.0.1:8000/group/{group.id}/"
                send_notification(token, 'Новое сообщение', f'Новое сообщение от {instance.user.username}', 
                                  click_action_url=message_url)

                
                
                

def showFirebaseJS(request):
    data = (
        'importScripts("https://www.gstatic.com/firebasejs/8.6.3/firebase-app.js");'
        'importScripts("https://www.gstatic.com/firebasejs/8.6.3/firebase-messaging.js"); '
        'const firebaseConfig = {'
        '    apiKey: "AIzaSyAGY1ytwc1uWbaj0Irr9-91kcR2suSQxvo",'
        '    authDomain: "chat-1a046.firebaseapp.com",'
        '    projectId: "chat-1a046",'
        '    storageBucket: "chat-1a046.appspot.com",'
        '    messagingSenderId: "100039898809",'
        '    appId: "1:100039898809:web:d75ce071caadd3c8924d68",'
        '    measurementId: "G-PY30DVF1J3"'
        '};'
        'firebase.initializeApp(firebaseConfig);'
        'const messaging = firebase.messaging();'
        'messaging.onBackgroundMessage(function (payload) {'
        '    console.log(payload);'
        '    const notification = payload.notification;'
        '    const notificationOptions = {'
        '        body: notification.body,'
        '        icon: notification.icon || "https://cdn-icons-png.flaticon.com/512/5356/5356355.png",'
        '        image: notification.image || "https://img.freepik.com/free-photo/reminder-popup-bell-notification-alert-or-alarm-icon-sign-or-symbol-for-application-website-ui-on-purple-background-3d-rendering-illustration_56104-1304.jpg",'
        '        data: {'
        '            url: notification.click_action || "/"'  # Добавляем URL для перехода
        '        }'
        '    };'
        '    self.registration.showNotification(notification.title, notificationOptions);'
        '});'

        'self.addEventListener("notificationclick", function(event) {'
        '    event.notification.close();'
        '    const url = event.notification.data.url;'
        '    event.waitUntil('
        '        clients.matchAll({ type: "window", includeUncontrolled: true }).then( windowClients => {'
        '            for (let client of windowClients) {'
        '                if (client.url === url && "focus" in client) {'
        '                    return client.focus();'
        '                }'
        '            }'
        '            if (clients.openWindow) {'
        '                return clients.openWindow(url);'
        '            }'
        '        })'
        '    );'
        '});'
    )

    return HttpResponse(data, content_type="text/javascript")



