from rest_framework import status
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from django.http import Http404
from Api.models import Role


def permission_required(perm):
    def inner(function):
        def wrapper(self, *args, **kwargs):
            perm_li = []
            for role in self.request.user.roles.all():
                role_permissions = role.permissions.all()
                for permission in role_permissions:
                    perm_li.append(permission.code_name)
            for p in perm:
                has_perm = p in perm_li
                if has_perm:
                    return function(self, *args, **kwargs)
            raise PermissionDenied
        return wrapper
    return inner