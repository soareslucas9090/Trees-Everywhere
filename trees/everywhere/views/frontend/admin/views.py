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


class MenuAdminView(View):
    def get(self, request):
        return render(request, "admin/menu.html")


@method_decorator(csrf_protect, name="dispatch")
class Redirect(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if IsAdmin():
                return redirect("menu_admin")
            else:
                ...
        else:
            return redirect("login")


class UserCreateView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, "admin/forms/registration_form.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user_create")
        return render(request, "admin/forms/registration_form.html", {"form": form})


class AccountListView(View):
    def get(self, request):
        accounts = Account.objects.all()
        return render(request, "admin/lists/account_list.html", {"accounts": accounts})

    def post(self, request):
        account_id = request.POST.get("account_id")
        account = get_object_or_404(Account, id=account_id)
        account.active = not account.active
        account.save()
        return redirect("accounts_list")


class AccountCreateView(View):
    def get(self, request):
        form = AccountForm()
        return render(request, "admin/forms/account_form.html", {"form": form})

    def post(self, request):
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts_list")
        return render(request, "admin/forms/account_form.html", {"form": form})


class TreeListView(View):
    def get(self, request):
        trees = Tree.objects.all()
        return render(request, "admin/lists/tree_list.html", {"trees": trees})


class TreeCreateView(View):
    def get(self, request):
        form = TreeForm()
        return render(request, "admin/forms/tree_form.html", {"form": form})

    def post(self, request):
        form = TreeForm(request.POST)
        if form.is_valid():
            form.save()
            print(form)
            return redirect("trees_list")
        return render(request, "admin/lists/tree_form.html", {"form": form})


class TreeDetailView(View):
    def get(self, request, pk):
        tree = get_object_or_404(Tree, id=pk)
        planted_trees = PlantedTree.objects.filter(tree=tree)
        return render(
            request,
            "admin/details/tree_detail.html",
            {"tree": tree, "planted_trees": planted_trees},
        )
