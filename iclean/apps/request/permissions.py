from rest_framework import permissions


CREATE_METHOD = 'POST'
DELETE_METHOD = 'DELETE'

class IsStaffOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and (request.user.is_staff or request.method in permissions.SAFE_METHODS))

    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_authenticated and (request.user.is_staff or request.method in permissions.SAFE_METHODS))


class IsStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_authenticated and request.user.is_staff)


class IsClient(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role.role == "client")

    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_authenticated and request.user.role.role == "client" and request.user == obj.client.user)


class IsCompany(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role.role == "company" and request.method is not CREATE_METHOD)

    def has_object_permission(self, request, view, obj):

        return bool(request.user.is_authenticated and request.user.role.role == "company" and \
            request.user.id == obj.service.company.user.id and request.method is not DELETE_METHOD)