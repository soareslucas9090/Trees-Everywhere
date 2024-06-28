from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect

from ...models import Account


@method_decorator(csrf_protect, name="dispatch")
class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")


def index(request):
    context = {
        "teste1": 10,
        "teste": 20,
    }

    return render(request, "index.html", context=context)
