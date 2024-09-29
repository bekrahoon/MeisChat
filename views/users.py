from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from chat.forms import (
    CustomAuthenticationForm,
    MyUserCreationForm,
    ProfileUpdateForm,
)
from chat.models import MyUser, GroupIs, Message
from .otp import generate_otp, send_otp_via_email, send_otp_via_sms


def loginPage(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            otp = generate_otp()
            request.session["otp"] = otp

            # Отправка OTP пользователю
            if user.phone_number:
                send_otp_via_sms(user.phone_number, otp)
                messages.success(request, "OTP sent to your phone.")
            elif user.email:
                send_otp_via_email(user.email, otp)
                messages.success(request, "OTP sent to your email.")
            else:
                messages.error(
                    request, "No contact information associated with this account."
                )

            request.session["otp_user_id"] = user.id

            return redirect("verify_otp")
        else:
            messages.error(request, "Invalid login credentials.")
    else:
        form = CustomAuthenticationForm()

    context = {"page": page, "form": form}
    return render(request, "base/login.html", context)


def change_login(request):
    # Очистка сессии для удаления OTP информации
    request.session.pop("otp_user_id", None)

    # Перенаправление на страницу входа
    return redirect("login")


def suspended_view(request):
    return render(
        request,
        "base/suspended.html",
        {
            "message": "Ваш аккаунт был приостановлен. Свяжитесь с поддержкой для получения информации."
        },
    )


def registerPage(request):
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = MyUserCreationForm()

    context = {"form": form}
    return render(request, "base/register.html", context)


def logoutUser(request):
    logout(request)
    return redirect("home")


def participants(request, pk):

    if request.user.is_authenticated != True:
        return redirect("login")

    q = request.GET.get("q") if request.GET.get("q") != None else ""
    groups = GroupIs.objects.filter(
        Q(name__icontains=q) | Q(description__icontains=q),
        Q(participants__id=request.user.id) | Q(host=request.user),
    ).distinct()

    group_count = groups.count()
    group_messages = Message.objects.filter(Q(group__name__icontains=q))
    group = GroupIs.objects.get(id=pk)
    group_messages = group.chat_messages.order_by("-created")
    participants = group.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user, group=group, body=request.POST.get("body")
        )
        if message:
            print("Сообщение успешно сохранено:", message.body)
        else:
            print("Ошибка при сохранении сообщения")
        group.participants.add(request.user)
        return redirect("group", pk=group.id)

    context = {
        "group": group,
        "group_messages": group_messages,
        "participants": participants,
        "groups": groups,
        "group_count": group_count,
        "group_messages": group_messages,
    }

    return render(request, "base/participants.html", context)


def userProfile(request, pk):
    user = get_object_or_404(MyUser, id=pk)
    if request.method == "POST":
        if "update_profile" in request.POST:
            form = MyUserCreationForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect("user_profile", pk=user.id)
        elif "send_sms" in request.POST:
            otp = (
                generate_otp()
            )  # Генерация OTP, добавьте эту функцию, если она не определена
            if user.phone_number:
                send_otp_via_sms(user.phone_number, otp)
                messages.success(request, "SMS sent successfully!")
            else:
                messages.error(request, "No phone number associated with this account.")
            return redirect("user_profile", pk=user.id)
    else:
        form = MyUserCreationForm(instance=user)

    groups = user.groupis_set.all()
    group_messages = user.message_set.order_by("-created")

    context = {
        "user": user,
        "groups": groups,
        "group_messages": group_messages,
        "form": form,
    }
    return render(request, "base/profile.html", context)


@login_required
def profile_update(request, pk):
    user = get_object_or_404(MyUser, id=pk)

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("user_profile", pk=user.pk)
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = ProfileUpdateForm(instance=user)

    context = {
        "user": user,
        "form": form,
    }

    return render(request, "base/profile.html", context)
