from rest_framework import permissions


class AnonCreateAndUpdateOwnerOnly(permissions.BasePermission):
    """
    Custom permission:
        - allow anonymous POST
        - allow authenticated GET and PUT on *own* record
        - allow all actions for staff
    """

    def has_permission(self, request, view):
        # 익명 유저를 위한 조회
        return (
            view.action in [
                "list", "retrieve"] or request.user and request.user.is_authenticated
        )  # 유저에 의한 수정

    def has_object_permission(self, request, view, obj):
        breakpoint()
        if view.action in ["list", "retrieve"]:
            return True
        return (
            view.action in ["create", "update", "partial_update"]
            and obj.id == request.user.id
            or request.user.is_staff
        )


class AnonCreateAndUpdateOwnerOnlyWithMethod(permissions.BasePermission):
    """
    Custom permission:
        - allow anonymous POST
        - allow authenticated GET and PUT on *own* record
        - allow all actions for staff
    """

    def has_permission(self, request, view):
        return request.method == "POST" or request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in [
                "GET", "PUT", "PATCH"] and obj.id == request.user.id or request.user.is_staff
        )
