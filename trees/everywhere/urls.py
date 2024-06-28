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
from .views.frontend.views import CustomLogoutView, index

everywhere_router = SimpleRouter()
everywhere_router.register("users", UserViewSet)
everywhere_router.register("accounts", AccountViewSet)
everywhere_router.register("profiles", ProfileViewSet)
everywhere_router.register("trees", TreeViewSet)
everywhere_router.register("plantedtrees", PlantedTreeViewSet)

urlpatterns = [
    path("api/v1/", include(everywhere_router.urls)),
    path("index/", index, name="index"),
    path("", auth_views.LoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
]
