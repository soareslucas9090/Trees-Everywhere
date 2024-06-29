from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views.api.views import (
    AccountViewSet,
    PlantedTreeViewSet,
    ProfileViewSet,
    TreeViewSet,
    UserViewSet,
)
from .views.frontend.admin.views import (
    AccountCreateView,
    AccountListView,
    MenuAdminView,
    TreeCreateView,
    TreeDetailView,
    TreeListView,
    UserCreateView,
)
from .views.frontend.users.views import (
    MenuUserView,
    PlantedTreeAccountsView,
    PlantedTreeCreateView,
    PlantedTreeDetailView,
    PlantedTreeListView,
)
from .views.frontend.views import CustomLogoutView, RedirectView

everywhere_router = SimpleRouter()
everywhere_router.register("users", UserViewSet)
everywhere_router.register("accounts", AccountViewSet)
everywhere_router.register("profiles", ProfileViewSet)
everywhere_router.register("trees", TreeViewSet)
everywhere_router.register("plantedtrees", PlantedTreeViewSet)

urlpatterns = [
    ####### API #######
    path("api/v1/", include(everywhere_router.urls)),
    ####### Front #######
    ####### Auth #######
    path("", RedirectView.as_view(), name="start"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    ####### Admin #######
    path("menu/admin", MenuAdminView.as_view(), name="menu_admin"),
    path("user/create/", UserCreateView.as_view(), name="user_create"),
    path("accounts/", AccountListView.as_view(), name="accounts_list"),
    path("accounts/create/", AccountCreateView.as_view(), name="account_create"),
    path("trees/", TreeListView.as_view(), name="trees_list"),
    path("trees/create/", TreeCreateView.as_view(), name="tree_create"),
    path("trees/<int:pk>/", TreeDetailView.as_view(), name="tree_detail"),
    ####### User #######
    path("menu/user", MenuUserView.as_view(), name="menu_user"),
    path("planted_tree", PlantedTreeListView.as_view(), name="planted_trees_list"),
    path(
        "planted_tree/<int:pk>/",
        PlantedTreeDetailView.as_view(),
        name="planted_tree_detail",
    ),
    path(
        "planted_tree/create/",
        PlantedTreeCreateView.as_view(),
        name="planted_tree_create",
    ),
    path(
        "planted_tree/accounts/",
        PlantedTreeAccountsView.as_view(),
        name="planted_trees_list_account",
    ),
]
