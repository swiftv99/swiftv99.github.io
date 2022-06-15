from rest_framework import permissions


class IsStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_authenticated and request.user.is_staff)


class IsClient(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role.role == "client" and request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_authenticated and request.user.role.role == "client" and request.method in permissions.SAFE_METHODS)


class IsCompany(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role.role == "company")

    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_authenticated and request.user.role.role == "company" and request.user == obj.company.user)