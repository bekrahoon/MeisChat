from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.core.mail import send_mail
from twilio.rest import Client
from django.conf import settings
import random

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








def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    q = request.GET.get('q') if request.GET.get('q') else ''
    
    # Поиск по группам
    groups = GroupIs.objects.filter(
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    
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
        'users': users,  # Добавление найденных пользователей в контекст
        'q': q  # Передача строки поиска в контекст для отображения в шаблоне
    }
    
    return render(request, 'base/home.html', context)




def group(request, pk):    
    
    if request.user.is_authenticated !=  True:
        return redirect('login')
    
    page = 'participants'
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    groups = GroupIs.objects.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) 
    )
    
    group_count = groups.count()
    group_messages = Message.objects.filter(
        Q(group__name__icontains = q)
        )
    
    
    
    group = GroupIs.objects.get(id=pk)
    group_messages = group.message_set.all()
    participants = group.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            group=group,
            body=request.POST.get('body'),
            image=request.FILES.get('image'),
            video=request.FILES.get('video'),
            file=request.FILES.get('file')  # Обработка любых файлов
        )
        group.participants.add(request.user)
        return redirect('group', pk=group.id)



    context = {'group':group, 'group_messages':group_messages,
               'participants':participants,
               'groups':groups, 
               'group_count':group_count, 
               'group_messages':group_messages,
               'page':page}
    
    return render(request, 'base/group.html', context)

def participants(request, pk):    
    
    if request.user.is_authenticated !=  True:
        return redirect('login')
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    groups = GroupIs.objects.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) 
    )
    
    group_count = groups.count()
    group_messages = Message.objects.filter(
        Q(group__name__icontains = q)
        )
    
    
    
    group = GroupIs.objects.get(id=pk)
    group_messages = group.message_set.all()
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


@login_required
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
    group_messages = user.message_set.all()
    
    context = {
        'user': user,
        'groups': groups,
        'group_messages': group_messages,
        'form': form
    }
    return render(request, 'base/profile.html', context)



@login_required
def profile_view(request, pk):
    user = get_object_or_404(MyUser, pk=pk)
    
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


@login_required(login_url = 'login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')
    
    if request.method == 'POST':
        message.delete() 
        return redirect('home')
    return render(request, "base/delete.html", {'obj':message})


