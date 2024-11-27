from rest_framework.permissions import BasePermission

class SuperAdminPermission(BasePermission):
    """
    Yalnızca süper admin kullanıcılara izin veren özel bir yapı
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
