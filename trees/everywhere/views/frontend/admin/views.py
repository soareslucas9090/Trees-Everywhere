from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect

from ....forms import AccountForm, TreeForm, UserCreationForm
from ....models import Account, PlantedTree, Tree
from ....permissions import IsAdmin


def isAdmin(request, toRender):
    if IsAdmin().has_permission(request=request, view=None):
        print("200")
        context = None
        if len(toRender) > 1:
            context = toRender[1]
        return render(request=request, template_name=toRender[0], context=context)
    else:
        print(request.user)
        print("403")
        return HttpResponseForbidden()


@method_decorator(csrf_protect, name="dispatch")
class MenuAdminView(View):
    def get(self, request):
        return isAdmin(request, ["admin/menu.html"])


@method_decorator(csrf_protect, name="dispatch")
class UserCreateView(View):
    def get(self, request):
        form = UserCreationForm()
        return isAdmin(request, ["admin/forms/registration_form.html", {"form": form}])

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user_create")
        return isAdmin(request, ["admin/forms/registration_form.html", {"form": form}])


@method_decorator(csrf_protect, name="dispatch")
class AccountListView(View):
    def get(self, request):
        accounts = Account.objects.all()
        return isAdmin(
            request, ["admin/lists/account_list.html", {"accounts": accounts}]
        )

    def post(self, request):
        account_id = request.POST.get("account_id")
        account = get_object_or_404(Account, id=account_id)
        account.active = not account.active
        account.save()
        return redirect("accounts_list")


@method_decorator(csrf_protect, name="dispatch")
class AccountCreateView(View):
    def get(self, request):
        form = AccountForm()
        return isAdmin(request, ["admin/forms/account_form.html", {"form": form}])

    def post(self, request):
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts_list")
        return isAdmin(request, ["admin/forms/account_form.html", {"form": form}])


@method_decorator(csrf_protect, name="dispatch")
class TreeListView(View):
    def get(self, request):
        trees = Tree.objects.all()
        return isAdmin(request, ["admin/lists/tree_list.html", {"trees": trees}])


@method_decorator(csrf_protect, name="dispatch")
class TreeCreateView(View):
    def get(self, request):
        form = TreeForm()
        return isAdmin(request, ["admin/forms/tree_form.html", {"form": form}])

    def post(self, request):
        form = TreeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("trees_list")
        return isAdmin(request, ["admin/lists/tree_form.html", {"form": form}])


@method_decorator(csrf_protect, name="dispatch")
class TreeDetailView(View):
    def get(self, request, pk):
        tree = get_object_or_404(Tree, id=pk)
        planted_trees = PlantedTree.objects.filter(tree=tree)
        return isAdmin(
            request,
            [
                "admin/details/tree_detail.html",
                {"tree": tree, "planted_trees": planted_trees},
            ],
        )
