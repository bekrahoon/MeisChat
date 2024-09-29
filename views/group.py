    
def group_view(request, pk):
    group = GroupIs.objects.get(pk=pk)
    messages = Message.objects.filter(group=group).order_by("created")
    context = {"group": group, "messages": messages}

    return render(request, "base/group.html", context)



@login_required(login_url="login")
def createGroup(request):
    form = GroupIsForm()
    if request.method == "POST":
        form = GroupIsForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.host = request.user
            group.save()
            return redirect("home")

    context = {"form": form}
    return render(request, "base/group_form.html", context)


@login_required(login_url="login")
def updateGroup(request, pk):
    group = GroupIs.objects.get(id=pk)
    form = GroupIsForm(instance=group)

    if request.user != group.host:
        return HttpResponse("You are not allowed here!!")

    if request.method == "POST":
        form = GroupIsForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form}

    return render(request, "base/group_form.html", context)


@login_required(login_url="login")
def deleteGroup(request, pk):
    group = GroupIs.objects.get(id=pk)
    if request.user != group.host:
        return HttpResponse("You are not allowed here!!")

    if request.method == "POST":
        group.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": group})


def chat_file_upload(request, pk):
    if request.method == "POST" and request.FILES:
        try:
            file = request.FILES["file"]
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
                    "type": "chat_file",
                    "file_url": message.file.url,
                    "file_name": file_name,
                    "user": request.user.username,
                }
                async_to_sync(channel_layer.group_send)(f"group_{pk}", event)
                return JsonResponse(
                    {"file_url": message.file.url, "file_name": file_name}
                )
            else:
                return JsonResponse({"error": "Файл не был загружен"}, status=400)
        except Exception as e:
            # Логирование исключения и возврат ошибки
            print(f"Error in file upload: {e}")
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse(
        {"error": "Invalid request method or no file uploaded"}, status=400
    )
    
    
@login_required(login_url="login")
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You are not allowed here!!")

    if request.method == "POST":
        message.delete()

        # Получаем URL для редиректа из формы (или перенаправляем на главную, если его нет)
        next_url = request.POST.get("next", "home")
        return redirect(next_url)

    # Передаём реферер в форму для дальнейшего использования
    return render(
        request,
        "base/delete.html",
        {"obj": message, "next": request.META.get("HTTP_REFERER", "home")},
    )


@login_required
def update_message_status(request, message_id):
    if request.method == "POST":
        try:
            message = Message.objects.get(id=message_id)
            message.read = True
            message.save()
            return JsonResponse({"status": "success"})
        except Message.DoesNotExist:
            return JsonResponse({"error": "Message not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=400)


