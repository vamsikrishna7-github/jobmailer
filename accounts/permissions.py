from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerProfile(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # obj can be profile or any model with a profile/user relation
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'profile'):
            return getattr(obj.profile, 'user', None) == request.user
        return False

