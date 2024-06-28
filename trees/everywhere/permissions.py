from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        else:
            return request.user.is_admin


class AllowAny(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
