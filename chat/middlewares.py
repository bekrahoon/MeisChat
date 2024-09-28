from django.shortcuts import redirect
from django.urls import reverse


class CheckSuspendedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Исключаем перенаправление для страницы 'suspended'
        suspended_url = reverse("suspended")
        if request.path == suspended_url:
            return self.get_response(request)

        # Проверка приостановки пользователя
        if request.user.is_authenticated and request.user.is_suspended:
            return redirect(suspended_url)

        return self.get_response(request)