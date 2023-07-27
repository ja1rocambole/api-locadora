from rest_framework.permissions import BasePermission
from users.models import User


class PermissionForUserDetailAuthView(BasePermission):
    def has_object_permission(self, request, view, obj: User):
        if request.user.is_employee:
            return True
        if obj == request.user:
            return True

        return False
