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





    
