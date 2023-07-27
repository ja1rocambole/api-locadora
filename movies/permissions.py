from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import User


class PermissionForMovieAuthView(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.method == "POST" or request.method == "DELETE":
            if request.user.is_anonymous:
                return False
            user = User.objects.filter(username=request.user).first()

            return user.is_employee

        return False
