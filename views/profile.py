
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