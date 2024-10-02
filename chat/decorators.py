from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse
from typing import Callable, Any

def suspended_decorator(view_func: Callable[[HttpRequest, Any], HttpResponse]) -> Callable[[HttpRequest, Any], HttpResponse]:
    def wrapper(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated and request.user.is_suspended:
            return redirect('suspended')
        return view_func(request, *args, **kwargs)
    return wrapper
