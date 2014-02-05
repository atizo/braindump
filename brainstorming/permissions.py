from rest_framework import permissions

PERMISSION_MAP = 'drf_permission_map'
PERMISSION_PROJECT = 'prj'


class BrainstromPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        # List action is allowed only to admin users
        if view.action == 'list':
            return request.user and request.user.is_staff

        return True

    def has_object_permission(self, request, view, obj):
        # Allows access to admin users
        if request.user and request.user.is_staff:
            return True
        # Read and create permissions are allowed to any request,
        # so we'll always allow GET, HEAD, OPTIONS or POST requests
        if request.method in permissions.SAFE_METHODS + ['POST']:
            return True

        return obj.pk in request.session.get(PERMISSION_MAP, {}).get(PERMISSION_PROJECT, [])