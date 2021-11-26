from rest_framework.permissions import BasePermission


class CustomPermissions(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        if view.action == 'vote' or view.action == 'subscribe' or view.action == 'unsubscribe':
            return True

        return False
