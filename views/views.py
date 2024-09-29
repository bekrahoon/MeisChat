@login_required
def home(request):
    if not request.user.is_authenticated:
        return redirect("login")

    q = request.GET.get("q") if request.GET.get("q") else ""

    # Поиск по группам
    groups = GroupIs.objects.filter(
        Q(name__icontains=q) | Q(description__icontains=q),
        Q(participants__id=request.user.id) | Q(host=request.user),
    ).distinct()

    group_count = groups.count()

    # Поиск по сообщениям
    group_messages = Message.objects.filter(Q(group__name__icontains=q))

    # Поиск по пользователям
    users = MyUser.objects.filter(Q(username__icontains=q) | Q(email__icontains=q))

    context = {
        "groups": groups,
        "group_count": group_count,
        "group_messages": group_messages,
        "users": users,
        "q": q,  # Передача строки поиска в контекст для отображения в шаблоне
    }

    return render(request, "base/home.html", context)


@suspended_decorator
@login_required
def group(request, pk):

    if request.user.is_authenticated != True:
        return redirect("login")

    page = "participants"

    q = request.GET.get("q") if request.GET.get("q") != None else ""
    groups = GroupIs.objects.filter(
        Q(name__icontains=q) | Q(description__icontains=q),
        Q(participants__id=request.user.id) | Q(host=request.user),
    ).distinct()

    group_count = groups.count()
    group_messages = Message.objects.filter(Q(group__name__icontains=q))
    users = MyUser.objects.filter(Q(username__icontains=q) | Q(email__icontains=q))
    form = MessageCreationForm()
    group = GroupIs.objects.get(id=pk)
    group_messages = group.chat_messages.order_by("-created")
    participants = group.participants.all()
    if request.user.is_suspended:
        return HttpResponseForbidden("Ваш аккаунт приостановлен.")

    other_user = None
    if group.is_private:
        if request.user not in group.members.all():
            raise Http404()
        for member in group.members.all():
            if member != request.user:
                other_user = member
                break
    context = {
        "group": group,
        "group_messages": group_messages,
        "participants": participants,
        "groups": groups,
        "group_count": group_count,
        "page": page,
        "other_user": other_user,
        "users": users,
        "pk": pk,
        "form": form,
    }

    return render(request, "base/group.html", context)


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



@login_required
def get_or_create_chat(request, pk):
    if request.user.id == pk:
        return redirect("home")

    other_user = MyUser.objects.get(pk=pk)

    # Поиск существующего чата
    chat = (
        GroupIs.objects.filter(is_private=True, members=other_user)
        .filter(members=request.user)
        .first()
    )  # Получаем первый подходящий чат, если он есть

    # Если чат не найден, создаем новый
    if chat is None:
        chat = GroupIs.objects.create(is_private=True)
        chat.members.add(other_user, request.user)

    return redirect("group", chat.id)


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
    
    
def group_view(request, pk):
    group = GroupIs.objects.get(pk=pk)
    messages = Message.objects.filter(group=group).order_by("created")
    context = {"group": group, "messages": messages}

    return render(request, "base/group.html", context)