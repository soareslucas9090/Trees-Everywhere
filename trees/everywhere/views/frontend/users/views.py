from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect

from ....forms import AccountForm, TreeForm, UserCreationForm
from ....models import Account, PlantedTree, Tree
from ....permissions import IsAdmin


@method_decorator(csrf_protect, name="dispatch")
class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")
