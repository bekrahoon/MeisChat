from django.shortcuts import get_object_or_404, render, redirect
from django.http import  HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import  *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django_otp import user_has_device
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_htmx.middleware import HtmxMiddleware

def loginPage(request):
    page = 'login'
    
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user_has_device(user):
                otp_device = TOTPDevice.objects.get(user=user)
                if otp_device.verify_token(request.POST.get('otp')):
                    login(request, user)
                    return redirect('home')
                else:
                    form.add_error(None, "Invalid OTP")
            else:
                login(request, user)
                return redirect('home')
    else:
        form = CustomAuthenticationForm()
             
    context = {'page':page, 'form': form}
    return render(request,  'base/login_register.html', context)



def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = MyUserCreationForm()
            
    context  = {'form': form}
    return render(request, 'base/login_register.html', context)



def home(request):
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
    context = {'groups':groups, 
               'group_count':group_count, 
               'group_messages':group_messages}
    return render(request, 'base/home.html', context)





def group(request, pk):    
    
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
        group.participants.add(request.user)
        return redirect('group', pk=group.id)

    context = {'group':group, 'group_messages':group_messages,
               'participants':participants,
               'groups':groups, 
               'group_count':group_count, 
               'group_messages':group_messages,
               }
    
    return render(request, 'base/group.html', context)




def userProfile(request, pk):
    user = MyUser.objects.get(id=pk)
    groups = user.groupis_set.all()
    group_messages = user.message_set.all()
    context = {'user':user, 'groups':groups, 'group_messages':group_messages}
    return render(request, 'base/profile.html', context )



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