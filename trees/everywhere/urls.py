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
    CustomLogoutView,
    MenuAdminView,
    Redirect,
    TreeCreateView,
    TreeDetailView,
    TreeListView,
    UserCreateView,
)

everywhere_router = SimpleRouter()
everywhere_router.register("users", UserViewSet)
everywhere_router.register("accounts", AccountViewSet)
everywhere_router.register("profiles", ProfileViewSet)
everywhere_router.register("trees", TreeViewSet)
everywhere_router.register("plantedtrees", PlantedTreeViewSet)

urlpatterns = [
    ####### API #######
    path("api/v1/", include(everywhere_router.urls)),
    path("", Redirect.as_view(), name="start"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("menu/admin", MenuAdminView.as_view(), name="menu_admin"),
    path("user/create/", UserCreateView.as_view(), name="user_create"),
    path("accounts/", AccountListView.as_view(), name="accounts_list"),
    path("accounts/create/", AccountCreateView.as_view(), name="account_create"),
    path("trees/", TreeListView.as_view(), name="trees_list"),
    path("trees/create/", TreeCreateView.as_view(), name="tree_create"),
    path("trees/<int:pk>/", TreeDetailView.as_view(), name="tree_detail"),
]
