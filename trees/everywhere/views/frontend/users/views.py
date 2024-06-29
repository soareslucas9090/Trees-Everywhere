from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect

from ....forms import AccountForm, TreeForm, UserCreationForm
from ....models import Account, PlantedTree, Tree
from ....permissions import IsAdmin


class MenuUserView(View):
    def get(self, request):
        return render(request, "user/menu.html")


class PlantedTreeListView(View):
    def get(self, request):
        planted_trees = PlantedTree.objects.all()
        return render(
            request,
            "user/lists/planted_tree_list.html",
            {"planted_trees": planted_trees},
        )
