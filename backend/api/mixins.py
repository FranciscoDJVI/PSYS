from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from api.constants import REQUEST_ACTION


class PermissionMixin:
    """
    Mixin to set permissions based on action.
    """

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.action in REQUEST_ACTION:
            self.permission_classes = [IsAdminUser, IsAuthenticated]
        return super().get_permissions()


class AdminOnlyMixin:
    """
    Mixin to restrict access to admin users only.
    """

    def get_permissions(self):
        self.permission_classes = [IsAdminUser, IsAuthenticated]
        return super().get_permissions()


class AuthenticatedUserMixin:
    """
    Mixin to restrict access to authenticated users only.
    """

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
