from rest_framework import serializers

from .models import Account, Account_User, PlantedTree, Profile, Tree, User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "about", "user", "joined"]
        extra_kwargs = {"joined": {"read_only": True}}

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "accounts",
            "password",
            "profile",
        ]

    password = serializers.CharField(write_only=True)
    accounts = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(), many=True, allow_empty=True
    )
    profile = serializers.SerializerMethodField(read_only=True)

    def get_profile(self, obj):
        try:
            profile = Profile.objects.get(user=obj.id)
            dict = {"id": profile.id, "about": profile.about, "joined": profile.joined}
            return dict
        except:
            print("Aqui")
            return None

    def validate_password(self, value):
        password = value

        if len(password) < 6:
            raise serializers.ValidationError("Must have at least 6 chars.")

        return password


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "name",
            "created",
            "active",
            "count_users",
        ]

    count_users = serializers.SerializerMethodField(read_only=True)

    def get_count_users(self, obj):
        try:
            users = Account_User.objects.get(account=obj).count()
            dict = None
            dict = {"count_users": users}
            return dict
        except:
            return None


class Account_UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account_User
        fields = "__all__"


class TreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tree
        fields = ["id", "name", "scientific_name", "count_planteds"]

    count_planteds = serializers.SerializerMethodField(read_only=True)

    def get_count_planteds(self, obj):
        try:
            trees = PlantedTree.objects.get(tree=obj).count()
            dict = None
            dict = {"count_count_planteds": trees}
            return dict
        except:
            return None


class PlantedTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantedTree
        fields = [
            "id",
            "age",
            "planted_at",
            "user",
            "user_data",
            "tree",
            "tree_data",
            "account",
            "account_data",
            "latitude",
            "longitude",
        ]

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), allow_empty=False, write_only=True
    )
    tree = serializers.PrimaryKeyRelatedField(
        queryset=Tree.objects.all(), allow_empty=False, write_only=True
    )
    account = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(), allow_empty=False, write_only=True
    )

    user_data = serializers.SerializerMethodField(read_only=True)
    tree_data = serializers.SerializerMethodField(read_only=True)
    account_data = serializers.SerializerMethodField(read_only=True)

    def get_user_data(self, obj):
        try:
            user = User.objects.get(id=obj.user.id)
            dict = None
            dict = {"id": user.id, "name": user.name, "email": user.email}
            return dict
        except:
            return None

    def get_tree_data(self, obj):
        try:
            tree = Tree.objects.get(id=obj.tree.id)
            dict = None
            dict = {"id": tree.id, "name": tree.name}
            return dict
        except:
            return None

    def get_account_data(self, obj):
        try:
            account = Account.objects.get(id=obj.account.id)
            dict = None
            dict = {"id": account.id, "name": account.name}
            return dict
        except:
            return None


class PlantTree(serializers.Serializer):
    tree = serializers.PrimaryKeyRelatedField(
        queryset=Tree.objects.all(), allow_empty=False
    )
    location = serializers.ListField(
        child=serializers.DecimalField(max_digits=9, decimal_places=6),
        allow_empty=False,
    )
    age = serializers.IntegerField()
    account = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(), allow_empty=False
    )


class PlantTrees(serializers.Serializer):
    plants = serializers.ListSerializer(child=PlantTree())


class MyPlants(serializers.ModelSerializer):
    class Meta:
        model = PlantedTree
        fields = "__all__"
