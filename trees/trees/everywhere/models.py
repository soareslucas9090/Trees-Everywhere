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
        account,
        password=None,
        **extra_fields,
    ):
        if not name:
            raise ValueError("The user needs a valid name!")
        if not email:
            raise ValueError("The user needs a valid email!")
        if not account:
            raise ValueError("The user needs a valid account!")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            account=Account.objects.get(pk=account),
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        nome,
        account,
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
            account=account,
            password=password,
            **extra_fields,
        )

        permissions = Permission.objects.all()
        user.user_permissions.set(permissions)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(unique=True, null=False)
    account = models.ForeignKey(
        Account, related_name="user_account", on_delete=models.RESTRICT, null=False
    )
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
