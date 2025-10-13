from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission: only owners or admins can access/update/delete.
    """

    def has_object_permission(self, request, view, obj):
        # If obj is User model instance:
        if hasattr(obj, 'pk') and getattr(obj, 'username', None) is not None:
            # obj is a User instance
            return request.user.is_staff or obj == request.user
        # Otherwise assume task-like object with .owner
        return request.user.is_staff or (hasattr(obj, 'owner') and obj.owner == request.user)
