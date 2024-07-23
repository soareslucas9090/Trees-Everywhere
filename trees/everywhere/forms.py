from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError

from .models import Account, PlantedTree, Profile, Tree, User


class AdminPortalUserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email", "name", "is_admin", "is_superuser")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if user.is_superuser:
            user.is_admin = True
            user.is_staff = True
            permissions = Permission.objects.all()
            user.user_permissions.set(permissions)

        if commit:
            user.save()
        return user


class AdminPortalUserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", "password", "name", "is_active", "is_admin"]

    def save(self, commit=True):
        user = super().save(commit=False)

        if user.is_superuser:
            user.is_admin = True
            user.is_staff = True
            permissions = Permission.objects.all()
            user.user_permissions.set(permissions)

        else:
            user.is_staff = False
            none_permissions = Permission.objects.none()
            user.user_permissions.set(none_permissions)

        if commit:
            user.save()
        return user


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "email",
            "name",
            "password",
            "accounts",
        ]

    accounts = forms.ModelMultipleChoiceField(
        queryset=Account.objects.filter(active=True), required=False
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.password = make_password(password=user.password)
            user.save()
            self.save_m2m()
            user.accounts.set(self.cleaned_data["accounts"])
        return user


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["name", "active"]


class TreeForm(forms.ModelForm):
    class Meta:
        model = Tree
        fields = ["name", "scientific_name"]


class PlantedTreeForm(forms.ModelForm):
    class Meta:
        model = PlantedTree
        fields = ["age", "tree", "account", "latitude", "longitude"]

    def get_form(self):
        if self.is_valid():
            data = self.cleaned_data
            return data
        else:
            return None

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(PlantedTreeForm, self).__init__(*args, **kwargs)

        if user:
            self.fields["account"].queryset = Account.objects.filter(
                accountuser_account__user=user
            )

    tree = forms.ModelChoiceField(queryset=Tree.objects.all(), required=True)
    latitude = forms.DecimalField()
    longitude = forms.DecimalField()
