from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 읽기는 항상 허용한다.
        if request.method in permissions.SAFE_METHODS:
            return True
        # SAFE_METHODS 해당하지 않으면 작성자와 수정하려고 하는 자가 같아야 한다.
        return obj.owner == request.user


class IsVoterOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.voter == request.user
