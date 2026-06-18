"""
自定义权限类
"""
from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """只允许对象的所有者进行写操作"""

    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'owner_user_id'):
            return obj.owner_user_id == request.user.id
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user.id
        return False


class IsAdminUser(BasePermission):
    """只允许后台管理员访问"""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (request.user.is_admin or request.user.role in ('admin', 'editor', 'reviewer'))
        )


class IsSuperAdmin(BasePermission):
    """只允许超级管理员访问"""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_admin
            and request.user.role == 'admin'
        )


class IsPolicyEditor(BasePermission):
    """政策编辑权限"""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ('admin', 'editor')
        )


class IsPolicyReviewer(BasePermission):
    """政策审核权限"""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ('admin', 'reviewer')
        )


class IsTeamLeader(BasePermission):
    """小队队长权限"""

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'role'):
            return obj.role == 'leader' and obj.user == request.user
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user.id
        return False
