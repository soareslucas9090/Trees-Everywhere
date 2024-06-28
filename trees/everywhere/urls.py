from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views.api.views import (
    AccountViewSet,
    PlantedTreeViewSet,
    ProfileViewSet,
    TreeViewSet,
    UserViewSet,
)

everywhere_router = SimpleRouter()
everywhere_router.register("users", UserViewSet)
everywhere_router.register("accounts", AccountViewSet)
everywhere_router.register("profiles", ProfileViewSet)
everywhere_router.register("trees", TreeViewSet)
everywhere_router.register("plantedtrees", PlantedTreeViewSet)


urlpatterns = [
    path("", include(everywhere_router.urls)),
]
