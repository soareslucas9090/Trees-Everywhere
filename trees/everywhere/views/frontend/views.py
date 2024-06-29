from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect

from ...permissions import IsAdmin


@method_decorator(csrf_protect, name="dispatch")
class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")


@method_decorator(csrf_protect, name="dispatch")
class RedirectView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if IsAdmin().has_permission(request, View):
                return redirect("menu_admin")
            else:
                return redirect("menu_user")
        else:
            return redirect("login")
