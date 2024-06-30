from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiTypes,
    extend_schema,
    extend_schema_view,
)
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


@extend_schema_view(
    list=extend_schema(tags=["Users"]),
    retrieve=extend_schema(tags=["Users"]),
    create=extend_schema(tags=["Users"]),
    update=extend_schema(tags=["Users"]),
    partial_update=extend_schema(tags=["Users"]),
    destroy=extend_schema(tags=["Users"]),
)
@extend_schema(description="Only users with administrator permissions.")
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


@extend_schema_view(
    list=extend_schema(tags=["Accounts"]),
    retrieve=extend_schema(tags=["Accounts"]),
    create=extend_schema(tags=["Accounts"]),
    update=extend_schema(tags=["Accounts"]),
    partial_update=extend_schema(tags=["Accounts"]),
    destroy=extend_schema(tags=["Accounts"]),
)
@extend_schema(description="Only users with administrator permissions.")
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


@extend_schema_view(
    list=extend_schema(tags=["Profiles"]),
    retrieve=extend_schema(tags=["Profiles"]),
    create=extend_schema(tags=["Profiles"]),
    update=extend_schema(tags=["Profiles"]),
    partial_update=extend_schema(tags=["Profiles"]),
    destroy=extend_schema(tags=["Profiles"]),
)
@extend_schema(description="Only users with administrator permissions.")
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


@extend_schema_view(
    list=extend_schema(tags=["Trees"]),
    retrieve=extend_schema(tags=["Trees"]),
    create=extend_schema(tags=["Trees"]),
    update=extend_schema(tags=["Trees"]),
    partial_update=extend_schema(tags=["Trees"]),
    destroy=extend_schema(tags=["Trees"]),
)
@extend_schema(description="Only users with administrator permissions.")
class TreeViewSet(ModelViewSet):
    queryset = Tree.objects.all()
    serializer_class = TreeSerializer
    permission_classes = [
        IsAdmin,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        name = self.request.query_params.get("name", None)

        if name:
            queryset = queryset.filter(name__icontais=name)

        scientific_name = self.request.query_params.get("scientific_name", None)

        if scientific_name:
            queryset = queryset.filter(scientific_name__icontais=scientific_name)

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
                name="scientific_name",
                type=OpenApiTypes.STR,
                description="Filter by scientific name",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema_view(
    list=extend_schema(tags=["PlantedTrees"]),
    retrieve=extend_schema(tags=["PlantedTrees"]),
    create=extend_schema(tags=["PlantedTrees"]),
    update=extend_schema(tags=["PlantedTrees"]),
    partial_update=extend_schema(tags=["PlantedTrees"]),
    destroy=extend_schema(tags=["PlantedTrees"]),
)
@extend_schema(description="Only users with administrator permissions.")
class PlantedTreeViewSet(ModelViewSet):
    queryset = PlantedTree.objects.all()
    serializer_class = PlantedTreeSerializer
    permission_classes = [
        IsAdmin,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        user = self.request.query_params.get("user", None)

        if user:
            queryset = queryset.filter(user=user)

        user_name = self.request.query_params.get("user_name", None)

        if user_name:
            queryset = queryset.filter(user__name__icontains=user_name)

        tree = self.request.query_params.get("tree", None)

        if tree:
            queryset = queryset.filter(tree=tree)

        tree_name = self.request.query_params.get("tree_name", None)

        if tree_name:
            queryset = queryset.filter(tree__name__icontains=tree_name)

        tree_scientific_name = self.request.query_params.get(
            "tree_scientific_name", None
        )

        if tree_scientific_name:
            queryset = queryset.filter(
                tree__scientific_name__icontains=tree_scientific_name
            )

        account = self.request.query_params.get("account", None)

        if account:
            queryset = queryset.filter(account=account)

        account_name = self.request.query_params.get("account_name", None)

        if account_name:
            queryset = queryset.filter(account__name__icontains=account_name)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="user",
                type=OpenApiTypes.INT,
                description="Filter by user",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="user_name",
                type=OpenApiTypes.STR,
                description="Filter by user name",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="tree",
                type=OpenApiTypes.INT,
                description="Filter by tree",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="tree_name",
                type=OpenApiTypes.STR,
                description="Filter by tree name",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="tree_scientific_name",
                type=OpenApiTypes.STR,
                description="Filter by tree scientific name",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="account",
                type=OpenApiTypes.INT,
                description="Filter by account",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="account_name",
                type=OpenApiTypes.STR,
                description="Filter by account name",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema_view(
    create=extend_schema(tags=["PlantTree"]),
)
@extend_schema(description="Regular users only.")
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


@extend_schema_view(
    create=extend_schema(tags=["PlantTrees"]),
)
@extend_schema(description="Regular users only.")
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


@extend_schema_view(
    list=extend_schema(tags=["MyPlants"]),
)
@extend_schema(description="Regular users only.")
class MyPlantsViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = PlantedTree.objects.all()
    serializer_class = MyPlants
    permission_classes = [
        IsNormalUser,
    ]
    http_method_names = ["get"]

    def get_queryset(self):
        return PlantedTree.objects.filter(user=self.request.user)
