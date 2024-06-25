from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Permission,
    PermissionsMixin,
)
from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=255, null=False)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True, null=False)


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
        nome,
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
            nome=nome,
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
        return self.nome

    def save(self, *args, **kwargs):
        self.nome = self.nome.lower()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"


class Account_User(models.Model):
    account = models.ForeignKey(
        Account, related_name="accountuser_account", on_delete=models.CASCADE, null=False
    )
    user = models.ForeignKey(
        User, related_name="accountuser_user", on_delete=models.CASCADE, null=False
    )

    def __str__(self):
        str = f"Setor: {self.setor} e Usuario: {self.usuario}"
        return str


class Profile(models.Model):
    about = models.TextField(blank=False, null=False)
    joined = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="profile_user", on_delete=models.CASCADE, null=False)


class Tree(models.Model):
    name = models.CharField(max_length=255, null=False)
    scientific_name = models.CharField(max_length=255, null=False)


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
        Account, related_name="plantedtree_account", on_delete=models.RESTRICT, null=False
    )
