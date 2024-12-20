from rest_framework import permissions

from apps.users.models import CustomUser 



class IsOperatorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        elif request.user.role == CustomUser.RoleChoices.Operator:
            return True
        return False