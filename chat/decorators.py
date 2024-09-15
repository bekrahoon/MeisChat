from django.shortcuts import redirect

def suspended_decorator(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_suspended:
            return redirect('suspended')
        return view_func(request, *args, **kwargs)
    return wrapper









