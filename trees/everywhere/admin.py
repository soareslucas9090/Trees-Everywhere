from django.contrib import admin

from .models import Account, Account_User, PlantedTree, Profile, Tree, User


class UserAdmin(admin.ModelAdmin):
    pass


class AccountAdmin(admin.ModelAdmin):
    pass


class Account_UserAdmin(admin.ModelAdmin):
    pass


class ProfileAdmin(admin.ModelAdmin):
    pass


class TreeAdmin(admin.ModelAdmin):
    pass


class PlantedTreeAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Account_User, Account_UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tree, TreeAdmin)
admin.site.register(PlantedTree, PlantedTreeAdmin)
