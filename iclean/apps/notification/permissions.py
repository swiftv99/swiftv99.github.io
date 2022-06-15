from rest_framework import permissions


class IsStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_authenticated and request.user.is_staff)


class IsSender(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated )

    def has_object_permission(self, request, view, obj):
        if request.user == obj.sender:
            return True
        return request.method in permissions.SAFE_METHODS