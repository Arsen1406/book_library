from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != 'GET':
            return request.user.is_staff
        return True


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class AdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.reader == request.user
