from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.views import View
from chat.models import MyUser
from twilio.rest import Client
import random
import logging


def generate_otp():
    return random.randint(100000, 999999)


def send_otp_via_email(email, otp):
    logger.debug(f"Sending OTP {otp} to email {email}")
    subject = "Your OTP Code"
    message = f"Your OTP is {otp}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


def send_otp_via_sms(phone_number, otp):
    logger.debug(f"Sending OTP {otp} to phone number {phone_number}")
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your OTP is {otp}", from_=settings.TWILIO_PHONE_NUMBER, to=phone_number
    )
    return message.sid


logger = logging.getLogger(__name__)


class VerifyOTPView(View):
    def post(self, request):
        otp_input = request.POST.get("otp")
        user_id = request.session.get("otp_user_id")
        session_otp = request.session.get("otp")

        logger.debug(
            f"User ID: {user_id}, Input OTP: {otp_input}, Session OTP: {session_otp}"
        )

        if not user_id:
            messages.error(request, "User session not found")
            return redirect("login")

        user = get_object_or_404(MyUser, id=user_id)

        # Преобразуем значения в строки перед сравнением
        if session_otp and str(otp_input).strip() == str(session_otp).strip():
            login(request, user)
            request.session.pop("otp_user_id", None)
            request.session.pop("otp", None)
            messages.success(request, "Successfully logged in")
            return redirect("home")
        else:
            logger.error("Invalid OTP Error")
            messages.error(request, "Invalid OTP")
            return redirect("verify_otp")

    def get(self, request):
        user_id = request.session.get("otp_user_id")
        user = get_object_or_404(MyUser, id=user_id) if user_id else None
        context = {"user": user}
        return render(request, "base/login.html", context)


def resend_otp(request):
    user_id = request.session.get("otp_user_id")
    if not user_id:
        messages.error(request, "User session not found")
        return redirect("login")

    user = get_object_or_404(MyUser, id=user_id)
    otp = generate_otp()  # Генерируем новый OTP

    # Преобразуйте OTP в строку перед сохранением в сессии
    request.session["otp"] = str(otp)

    if user.phone_number:
        send_otp_via_sms(user.phone_number, otp)
    elif user.email:
        send_otp_via_email(user.email, otp)
    else:
        messages.error(request, "No contact information associated with this account.")
        return redirect("verify_otp")

    logger.debug(f"New OTP: {otp} saved in session")
    messages.success(request, "OTP has been resent to your email or phone.")
    return redirect("verify_otp")
