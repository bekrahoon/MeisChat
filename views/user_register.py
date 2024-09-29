
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


logger = logging.getLogger(__name__)


def verify_otp(request):
    if request.method == "POST":
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

        # Преобразуйте значения в строки перед сравнением
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

def suspended_view(request):
    return render(
        request,
        "base/suspended.html",
        {
            "message": "Ваш аккаунт был приостановлен. Свяжитесь с поддержкой для получения информации."
        },
    )