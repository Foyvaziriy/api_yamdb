from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from django.http import HttpRequest
from django.db.models import Model


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, view: ModelViewSet) -> bool:
        return (
            request.user.is_authenticated and (request.user.role == 'admin')
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, view: ModelViewSet) -> bool:
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.role == 'admin')
        )


class AuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, view: ModelViewSet) -> bool:
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self,
                              request: HttpRequest,
                              view: ModelViewSet,
                              obj: Model) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        return any([
            obj.author == request.user,
            request.user.role in ['moderator', 'admin']
        ])
