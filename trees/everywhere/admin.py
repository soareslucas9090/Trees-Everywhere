from typing import Any

from django.contrib import admin
from django.contrib.auth.models import Group
from django.http import HttpRequest

from .forms import AdminPortalUserChangeForm, AdminPortalUserCreationForm
from .models import Account, Account_User, PlantedTree, Profile, Tree, User


class AccountUserInline(admin.TabularInline):
    model = Account_User
    extra = 1


class UserAdmin(admin.ModelAdmin):
    form = AdminPortalUserChangeForm
    add_form = AdminPortalUserCreationForm

    # Overlapping function to customize the user addition forms.
    def get_form(self, request, obj=None, **kwargs):
        if obj:
            return super().get_form(request, obj, **kwargs)
        else:
            return self.add_form

    # Overlapping function to customize the user addition fieldset.
    def get_fieldsets(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> list[tuple[str | None, dict[str, Any]]]:
        if obj:
            return super().get_fieldsets(request, obj)
        else:
            return self.add_fieldsets

    # Customizing actions
    actions = ["make_active", "make_inactive"]

    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    make_active.short_description = "Marcar usuários selecionados como ativos"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    make_inactive.short_description = "Marcar usuários selecionados como inativos"

    list_display = (
        "name",
        "email",
        "date_joined",
        "is_active",
        "is_admin",
        "is_superuser",
    )
    list_filter = ("is_active", "is_admin", "is_staff")
    inlines = [AccountUserInline]

    # Fieldsets for listing or updating.
    fieldsets = [
        ("Credentials", {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ("name",)}),
        ("Permissions", {"fields": ("is_admin", "is_superuser")}),
    ]

    # Fieldsets for creation.
    add_fieldsets = [
        (
            "Credentials",
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "password1",
                    "password2",
                ],
            },
        ),
        ("Personal info", {"fields": ("name",)}),
        ("Permissions", {"fields": ("is_admin", "is_superuser")}),
    ]

    search_fields = ("email", "name")
    ordering = ("name",)


class AccountAdmin(admin.ModelAdmin):
    list_display = ("name", "created", "active")
    search_fields = ("name",)
    list_filter = ("active",)
    inlines = [AccountUserInline]


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "about",
        "joined",
    )
    fieldsets = [
        ("None", {"fields": ["about", "user"]}),
    ]
    search_fields = ("about",)


class TreeAdmin(admin.ModelAdmin):
    list_display = ("name", "scientific_name")
    search_fields = ("name", "scientific_name")


class PlantedTreeAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "tree",
        "age",
        "latitude",
        "longitude",
        "planted_at",
        "account",
    )
    search_fields = ("user__name", "tree__name", "account__name")
    list_filter = ("age", "planted_at")


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tree, TreeAdmin)
admin.site.register(PlantedTree, PlantedTreeAdmin)
