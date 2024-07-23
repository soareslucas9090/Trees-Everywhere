from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Permission,
    PermissionsMixin,
)
from django.db import models, transaction


class Account(models.Model):
    name = models.CharField(max_length=255, null=False)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True, null=False)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        name,
        password=None,
        **extra_fields,
    ):
        if not name:
            raise ValueError("The user needs a valid name!")
        if not email:
            raise ValueError("The user needs a valid email!")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        name,
        password=None,
        **extra_fields,
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_admin") is not True:
            raise ValueError("Superuser must have is_admin=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        user = self.create_user(
            email=email,
            name=name,
            password=password,
            **extra_fields,
        )

        permissions = Permission.objects.all()
        user.user_permissions.set(permissions)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(unique=True, null=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    accounts = models.ManyToManyField("Account", through="Account_User", blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    REQUIRED_FIELDS = [
        "name",
    ]

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.name

    # Este método save salva o nome do usuário com tudo em minusculo
    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def plant_tree(self, tree, location, age, account):
        if isinstance(tree, int):
            PlantedTree.objects.create(
                user=self,
                tree=Tree.objects.get(id=tree),
                latitude=location[0],
                longitude=location[1],
                age=age,
                account=Account.objects.get(id=account),
            )
        elif isinstance(tree, Tree):
            PlantedTree.objects.create(
                user=self,
                tree=tree,
                latitude=location[0],
                longitude=location[1],
                age=age,
                account=account,
            )
        else:
            latitude = location.value[0]
            longitude = location.value[1]
            PlantedTree.objects.create(
                user=self,
                tree=Tree.objects.get(id=tree.value),
                latitude=latitude,
                longitude=longitude,
                age=age.value,
                account=Account.objects.get(id=account.value),
            )

    @transaction.atomic
    def plant_trees(self, trees_to_plant):
        try:
            for tree_to_plant in trees_to_plant.value:
                tree = tree_to_plant["tree"]
                location = tree_to_plant["location"]
                age = tree_to_plant["age"]
                account = tree_to_plant["account"]
                self.plant_tree(tree, location, age, account)
        except:
            for tree_to_plant in trees_to_plant:
                tree = tree_to_plant["tree"]
                location = tree_to_plant["location"]
                age = tree_to_plant["age"]
                account = tree_to_plant["account"]
                self.plant_tree(tree, location, age, account)


class Account_User(models.Model):
    account = models.ForeignKey(
        Account,
        related_name="accountuser_account",
        on_delete=models.CASCADE,
        null=False,
    )
    user = models.ForeignKey(
        User, related_name="accountuser_user", on_delete=models.CASCADE, null=False
    )

    def __str__(self):
        str = f"Account: {self.account}, User: {self.user}"
        return str


class Profile(models.Model):
    about = models.TextField(blank=False, null=False)
    user = models.OneToOneField(
        User, related_name="profile_user", on_delete=models.CASCADE, null=False
    )
    joined = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):

        # Update the 'joined' field with the user's 'date_joined'
        if self.joined == None:
            if self.user:
                self.joined = self.user.date_joined

        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.name


class Tree(models.Model):
    name = models.CharField(max_length=255, null=False)
    scientific_name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name


class PlantedTree(models.Model):
    age = models.IntegerField(null=False)
    planted_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, related_name="plantedtree_user", on_delete=models.RESTRICT, null=False
    )
    tree = models.ForeignKey(
        Tree, related_name="plantedtree_tree", on_delete=models.RESTRICT, null=False
    )
    account = models.ForeignKey(
        Account,
        related_name="plantedtree_account",
        on_delete=models.RESTRICT,
        null=False,
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=False)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=False)

    def __str__(self):
        return f"User: {self.user}, Tree: {self.tree}"
