from rest_framework import permissions


class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)


class IsAdmin(permissions.BasePermission):
    """
    Обеспечивает доступ только администратору.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Полный доступ администратору, а для остальных только безопасные методы.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin
        return request.method in permissions.SAFE_METHODS
