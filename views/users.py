from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from chat.forms import (
    CustomAuthenticationForm,
    MyUserCreationForm,
    ProfileUpdateForm,
)
from chat.models import MyUser, GroupIs
from .otp import generate_otp, send_otp_via_email, send_otp_via_sms


class LoginPageView(View):
    template_name = "base/login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home")
        form = CustomAuthenticationForm()
        return render(request, self.template_name, {"page": "login", "form": form})

    def post(self, request):
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

        return render(request, self.template_name, {"page": "login", "form": form})


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


class RegisterPageView(View):
    template_name = "base/register.html"

    def get(self, request):
        form = MyUserCreationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        return render(request, self.template_name, {"form": form})


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
    group = GroupIs.objects.get(id=pk)
    participants = group.participants.all()

    context = {
        "group": group,
        "participants": participants,
        "groups": groups,
    }
    return render(request, "base/participants.html", context)


class UserProfileView(View):
    template_name = "base/profile.html"

    def get_user(self, pk):
        return get_object_or_404(MyUser, id=pk)

    def get(self, request, pk):
        user = self.get_user(pk)
        form = MyUserCreationForm(instance=user)
        groups = user.groupis_set.all()
        group_messages = user.message_set.order_by("-created")

        context = {
            "user": user,
            "groups": groups,
            "group_messages": group_messages,
            "form": form,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        user = self.get_user(pk)

        if "update_profile" in request.POST:
            form = MyUserCreationForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect("user_profile", pk=user.id)

        elif "send_sms" in request.POST:
            otp = generate_otp()  # Генерация OTP
            if user.phone_number:
                send_otp_via_sms(user.phone_number, otp)
                messages.success(request, "SMS sent successfully!")
            else:
                messages.error(request, "No phone number associated with this account.")

            return redirect("user_profile", pk=user.id)

        # Если данные не валидны, рендерим форму снова с сообщением об ошибке
        form = MyUserCreationForm(instance=user)
        return render(request, self.template_name, {"user": user, "form": form})


class ProfileUpdateView(View):
    template_name = "base/profile.html"

    def get_user(self, pk):
        return get_object_or_404(MyUser, id=pk)

    def get(self, request, pk):
        user = self.get_user(pk)
        form = ProfileUpdateForm(instance=user)

        context = {
            "user": user,
            "form": form,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        user = self.get_user(pk)
        form = ProfileUpdateForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("user_profile", pk=user.pk)
        else:
            messages.error(request, "Please correct the error below.")

        context = {
            "user": user,
            "form": form,
        }
        return render(request, self.template_name, context)
