from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from ...models import Account, PlantedTree, Profile, Tree, User
from ...permissions import IsAdmin, IsNormalUser
from ...serializers import (
    AccountSerializer,
    MyPlants,
    PlantedTreeSerializer,
    PlantTree,
    PlantTrees,
    ProfileSerializer,
    TreeSerializer,
    UserSerializer,
)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAdmin,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        account = self.request.query_params.get("account", None)

        if account:
            queryset = queryset.filter(accounts__id=account)

        name = self.request.query_params.get("name", None)

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="account",
                type=OpenApiTypes.INT,
                description="Filter by account",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="name",
                type=OpenApiTypes.STR,
                description="Filter by name",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [
        IsAdmin,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        name = self.request.query_params.get("name", None)

        if name:
            queryset = queryset.filter(name__icontais=name)

        active = self.request.query_params.get("active", None)

        if active:
            if active.lower() == "false":
                active = "false"
            elif active.lower() == "true":
                active = "true"

            queryset = queryset.filter(active=active)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                type=OpenApiTypes.STR,
                description="Filter by name",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="active",
                type=OpenApiTypes.BOOL,
                description="Filter by active state",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [
        IsAdmin,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(id=serializer.data["user"])
        except:
            return Response(
                {"Error": "The User must be valid!"}, status=status.HTTP_404_NOT_FOUND
            )

        Profile.objects.create(
            about=serializer.data["about"],
            user=user,
            joined=user.date_joined,
        )
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class TreeViewSet(ModelViewSet):
    queryset = Tree.objects.all()
    serializer_class = TreeSerializer
    permission_classes = [
        IsAdmin,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]


class PlantedTreeViewSet(ModelViewSet):
    queryset = PlantedTree.objects.all()
    serializer_class = PlantedTreeSerializer
    permission_classes = [
        IsAdmin,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]


class PlantTreeViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = PlantedTree.objects.all()
    serializer_class = PlantTree
    permission_classes = [
        IsNormalUser,
    ]
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.plant_tree(
            tree=serializer["tree"],
            location=serializer["location"],
            age=serializer["age"],
            account=serializer["account"],
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class PlantTreesViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = PlantedTree.objects.all()
    serializer_class = PlantTrees
    permission_classes = [
        IsNormalUser,
    ]
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.plant_trees(trees_to_plant=serializer["plants"])
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class MyPlantsViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = PlantedTree.objects.all()
    serializer_class = MyPlants
    permission_classes = [
        IsNormalUser,
    ]
    http_method_names = ["get"]

    def get_queryset(self):
        return PlantedTree.objects.filter(user=self.request.user)
