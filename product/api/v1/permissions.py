from rest_framework.permissions import BasePermission, SAFE_METHODS
from courses.models import Subscription


def subscription(user, course_id: int) -> bool:
    if Subscription.objects.filter(user=user, course__id=course_id).exists():
        return True
    return False


class IsStudentOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return request.method in SAFE_METHODS and subscription(request.user, view.kwargs['course_id'])

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return request.method in SAFE_METHODS


class ReadOnlyOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS
