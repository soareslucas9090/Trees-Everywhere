from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect

from ....forms import PlantedTreeForm
from ....models import PlantedTree
from ....permissions import IsNormalUser


def isNormalUser(request, toRender):
    if IsNormalUser().has_permission(request=request, view=None):
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
class MenuUserView(View):
    def get(self, request):
        return isNormalUser(request, ["user/menu.html"])


@method_decorator(csrf_protect, name="dispatch")
class PlantedTreeListView(View):
    def get(self, request):
        planted_trees = PlantedTree.objects.filter(user=request.user)
        return isNormalUser(
            request,
            ["user/lists/planted_tree_list.html", {"planted_trees": planted_trees}],
        )


@method_decorator(csrf_protect, name="dispatch")
class PlantedTreeDetailView(View):
    def get(self, request, pk):
        planted_tree = get_object_or_404(PlantedTree, id=pk)
        return isNormalUser(
            request,
            ["user/detail/planted_tree_detail.html", {"planted_tree": planted_tree}],
        )


@method_decorator(csrf_protect, name="dispatch")
class PlantedTreeCreateView(View):
    def get(self, request):
        form = PlantedTreeForm(user=request.user)
        return isNormalUser(
            request, ["user/forms/planted_tree_forms.html", {"form": form}]
        )

    def post(self, request):
        form = PlantedTreeForm(request.POST, user=request.user)
        if form.is_valid():
            data_form = form.get_form()
            latitude = data_form["latitude"]
            longitude = data_form["longitude"]
            location = [latitude, longitude]
            request.user.plant_tree(
                tree=data_form["tree"],
                location=location,
                age=data_form["age"],
                account=data_form["account"],
            )
            return redirect("planted_trees_list")

        return isNormalUser(
            request, ["user/forms/planted_tree_forms.html", {"form": form}]
        )


@method_decorator(csrf_protect, name="dispatch")
class PlantedTreeAccountsView(View):
    def get(self, request):
        planted_trees = PlantedTree.objects.filter(
            account__in=request.user.accounts.all()
        )

        return isNormalUser(
            request,
            [
                "user/lists/planted_tree_list_account.html",
                {"planted_trees": planted_trees},
            ],
        )
