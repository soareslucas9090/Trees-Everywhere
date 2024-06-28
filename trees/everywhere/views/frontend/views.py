from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect

from ...forms import UserCreationForm
from ...models import Account
from ...permissions import IsAdmin


@method_decorator(csrf_protect, name="dispatch")
class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")


@method_decorator(csrf_protect, name="dispatch")
class Redirect(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if IsAdmin():
                return redirect("user_create")
            else:
                ...
        else:
            return redirect("login")


def index(request):
    context = {
        "teste1": 10,
        "teste": 20,
    }

    return render(request, "index.html", context=context)


class UserCreateView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, "admin/registration_form.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user_create")
        return render(request, "admin/registration_form.html", {"form": form})
