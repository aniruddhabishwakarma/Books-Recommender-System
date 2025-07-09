# decorators.py
from django.contrib.auth.decorators import user_passes_test

def admin_required(view_func=None, *, redirect_field_name="next", login_url="panel_login"):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )

    # If used as @admin_required without parentheses
    if view_func:
        return actual_decorator(view_func)

    # If used as @admin_required(...)
    return actual_decorator
