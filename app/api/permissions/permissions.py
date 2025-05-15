# app/api/permissions.py
from rest_framework import permissions

class IsSuperuserOrPerforador(permissions.BasePermission):
    """
    GETs abiertos; para POST/PUT/PATCH/DELETE solo superuser o username == 'perforador'.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        return bool(user and user.is_authenticated and (user.is_superuser or user.username.lower() == 'perforador'))


class IsSuperuserOrTatuador(permissions.BasePermission):
    """
    GETs abiertos; para POST/PUT/PATCH/DELETE solo superuser o username == 'perforador'.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        return bool(user and user.is_authenticated and (user.is_superuser or user.username.lower() == 'tatuador'))


class IsSuperuserOrTatuadorOrPerforador(permissions.BasePermission):
    """
    GETs abiertos; para POST/PUT/PATCH/DELETE superuser o username en ('tatuador','perforador').
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        return bool(
            user and user.is_authenticated and
            (user.is_superuser or user.username.lower() in ('tatuador','perforador'))
        )
