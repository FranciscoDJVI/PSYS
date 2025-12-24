from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated


class PermissionMixin:
    """
    Mixin to set permissions based on action.
    """

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST, PUT, PATCH, DELETE":
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
