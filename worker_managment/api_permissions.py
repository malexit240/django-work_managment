"""this module contains custom permissions for worker_managment app"""

from django.contrib.auth.models import User
from rest_framework import permissions


class IsManager(permissions.IsAuthenticated):
    """Checks that user is in a group 'Managers'"""

    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.groups.filter(name='Managers').exists()
