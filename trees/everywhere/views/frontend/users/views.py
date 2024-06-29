from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect

from ....forms import AccountForm, PlantedTreeForm, TreeForm, UserCreationForm
from ....models import Account, PlantedTree, Tree
from ....permissions import IsAdmin

@method_decorator(csrf_protect, name="dispatch")
class MenuUserView(View):
    def get(self, request):
        return render(request, "user/menu.html")

@method_decorator(csrf_protect, name="dispatch")
class PlantedTreeListView(View):
    def get(self, request):
        planted_trees = PlantedTree.objects.select_related("user").all()
        return render(
            request,
            "user/lists/planted_tree_list.html",
            {"planted_trees": planted_trees},
        )

@method_decorator(csrf_protect, name="dispatch")
class PlantedTreeDetailView(View):
    def get(self, request, pk):
        planted_tree = get_object_or_404(PlantedTree, id=pk)
        return render(
            request,
            "user/detail/planted_tree_detail.html",
            {"planted_tree": planted_tree},
        )

@method_decorator(csrf_protect, name="dispatch")
class PlantedTreeCreateView(View):
    def get(self, request):
        form = PlantedTreeForm(user=request.user)
        return render(request, "user/forms/planted_tree_forms.html", {"form": form})

    def post(self, request):
        form = PlantedTreeForm(request.POST, user=request.user)
        if form.is_valid():
            data_form = form.get_form()
            PlantedTree.objects.create(
                age=data_form["age"],
                user=request.user,
                tree=data_form["tree"],
                account=data_form["account"],
            )
            return redirect("planted_trees_list")

        return render(request, "user/forms/planted_tree_forms.html", {"form": form})

@method_decorator(csrf_protect, name="dispatch")
class PlantedTreeAccountsView(View):
    def get(self, request):
        planted_trees = PlantedTree.objects.all()

        print(PlantedTree.objects.filter(account__in=request.user.accounts.all()))
        return render(
            request,
            "user/lists/planted_tree_list_account.html",
            {"planted_trees": planted_trees},
        )
