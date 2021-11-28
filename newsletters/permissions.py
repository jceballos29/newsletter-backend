from rest_framework.permissions import BasePermission


class CustomPermissions(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'PUT'] and request.user.is_staff:
            return True

        if request.method == 'DELETE' and obj.created_by == request.user:
            return True

        if request.user.is_authenticated:
            return True

        if view.action == 'vote' or view.action == 'subscribe' or view.action == 'unsubscribe':
            return True

        return False
