from functools import wraps
from django.http import JsonResponse

def is_authenticated(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
    return _wrapped_view

def is_admin(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({'error': 'Permission denied'}, status=403)
    return _wrapped_view
