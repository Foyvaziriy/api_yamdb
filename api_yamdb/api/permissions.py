from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from django.http import HttpRequest


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, view: ModelViewSet) -> bool:
        return bool(request.user and (request.user.role == 'admin'))


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, view: ModelViewSet) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and (request.user.role == 'admin'))
