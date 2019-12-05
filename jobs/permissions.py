from rest_framework import permissions


class IsOwnerOrReadyOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.owner == request.user


class IsEmployer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user.employer


class IsEmployerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.user.employer
