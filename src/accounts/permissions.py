from functools import wraps

from django.core.exceptions import PermissionDenied

from .models import AccountProfile


def has_role(user, *roles):
    return user.is_authenticated and (
        user.is_superuser or user.account_profile.role in roles
    )


def role_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(request, *args, **kwargs):
            if not has_role(request.user, *roles):
                raise PermissionDenied
            return view(request, *args, **kwargs)

        return wrapped

    return decorator
