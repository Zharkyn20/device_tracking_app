from rest_framework import permissions


class IsCompany(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_company