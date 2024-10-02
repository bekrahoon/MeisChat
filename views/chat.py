from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import CreateView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from chat.forms import MessageCreationForm, GroupIsForm
from chat.models import MyUser, GroupIs, Message
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from chat.decorators import suspended_decorator
from typing import Optional, Dict, Any


@login_required
def home(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect("login")

    q: Optional[str] = request.GET.get("q") if request.GET.get("q") else ""

    # Поиск по группам
    groups = GroupIs.objects.filter(
        Q(name__icontains=q) | Q(description__icontains=q),
        Q(participants__id=request.user.id) | Q(host=request.user),
    ).distinct()

    group_count: int = groups.count()

    # Поиск по сообщениям
    group_messages = Message.objects.filter(Q(group__in=groups)).distinct()

    # Поиск по пользователям
    users = MyUser.objects.filter(Q(username__icontains=q) | Q(email__icontains=q))

    context: Dict[str, Any] = {
        "groups": groups,
        "group_count": group_count,
        "group_messages": group_messages,
        "users": users,
        "q": q,  # Передача строки поиска в контекст для отображения в шаблоне
    }

    return render(request, "base/home.html", context)


@suspended_decorator
@login_required
def group(request: HttpRequest, pk: int) -> HttpResponse:

    if request.user.is_authenticated != True:
        return redirect("login")

    page = "participants"

    q: Optional[str] = request.GET.get("q") if request.GET.get("q") != None else ""
    groups = GroupIs.objects.filter(
        Q(name__icontains=q) | Q(description__icontains=q),
        Q(participants__id=request.user.id) | Q(host=request.user),
    ).distinct()

    group_count: int = groups.count()
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
    context: Dict[str, Any] = {
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


@login_required
def get_or_create_chat(request: HttpRequest, pk: int) -> HttpResponse:
    if request.user.id == pk:
        return redirect("home")

    other_user: MyUser = MyUser.objects.get(pk=pk)

    # Поиск существующего чата
    chat: Optional[GroupIs] = (
        GroupIs.objects.filter(is_private=True, members=other_user)
        .filter(members=request.user)
        .first()
    )  # Получаем первый подходящий чат, если он есть

    # Если чат не найден, создаем новый
    if chat is None:
        chat = GroupIs.objects.create(is_private=True)
        chat.members.add(other_user, request.user)

    return redirect("group", chat.id)


class UpdateMessageStatusApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, message_id: int) -> Response:
        # Получаем сообщение или возвращаем 404, если оно не найдено
        message = get_object_or_404(Message, id=message_id)

        # Обновляем статус сообщения
        message.read = True
        message.save()
        # Возвращаем успешный ответ
        return Response({"status": "success"}, status=status.HTTP_200_OK)


class ChatFileUploadApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: HttpRequest, pk: int) -> Response:
        # Проверяем, содержит ли запрос файлы
        if request.FILES:
            try:
                file = request.FILES.get("file")
                file_name = file.name if file else None

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

                    # Возвращаем успешный ответ с информацией о файле
                    return Response(
                        {"file_url": message.file.url, "file_name": file_name},
                        status=status.HTTP_201_CREATED,
                    )
                else:
                    return Response(
                        {"error": "Файл не был загружен"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except Exception as e:
                # Логирование исключения и возврат ошибки
                print(f"Error in file upload: {e}")
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(
                {"error": "Invalid request method or no file uploaded"},
                status=status.HTTP_400_BAD_REQUEST,
            )


def group_view(request: HttpRequest, pk: int) -> HttpResponse:
    group = GroupIs.objects.get(pk=pk)
    messages = Message.objects.filter(group=group).order_by("created")
    context: Dict[str, Any] = {"group": group, "messages": messages}

    return render(request, "base/group.html", context)


class GroupCreateView(LoginRequiredMixin, CreateView):
    model = GroupIs
    form_class = GroupIsForm
    template_name = "base/group_form.html"
    login_url = "login"
    success_url = reverse_lazy("home")

    def form_valid(self, form: GroupIsForm) -> HttpResponse:
        # Устанавливаем текущего пользователя в качестве host
        form.instance.host = self.request.user
        return super().form_valid(form)


class GroupUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = GroupIs
    form_class = GroupIsForm
    template_name = "base/group_form.html"
    login_url = "login"
    success_url = reverse_lazy("home")

    def test_func(self) -> bool:
        # Проверяем, что текущий пользователь является хозяином группы
        group = self.get_object()
        return self.request.user == group.host

    def handle_no_permission(self) -> HttpResponse:

        return HttpResponse("You are not allowed here!!")


class GroupDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = GroupIs
    template_name = "base/delete.html"
    success_url = reverse_lazy("home")
    login_url = "login"

    def test_func(self) -> bool:
        # Проверяем, что текущий пользователь является хозяином группы
        group = self.get_object()
        return self.request.user == group.host

    def handle_no_permission(self) -> HttpResponse:
        return HttpResponse("You are not allowed here!!")


@login_required(login_url="login")
def deleteMessage(request: HttpRequest, pk: int):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You are not allowed here!!")

    if request.method == "POST":
        message.delete()

        # Получаем URL для редиректа из формы (или перенаправляем на главную, если его нет)
        next_url: str = request.POST.get("next", "home")
        return redirect(next_url)

    # Передаём реферер в форму для дальнейшего использования
    return render(
        request,
        "base/delete.html",
        {"obj": message, "next": request.META.get("HTTP_REFERER", "home")},
    )
