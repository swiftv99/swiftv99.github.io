from rest_framework import viewsets

from apps.user.models import Role
from apps.user.permissions import IsStaffOrReadOnly
from apps.user.serializers.role import AdminRoleSerializer, NonAdminRoleSerializer


# Role model
class RoleViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list', 'create', 'retrieve',
    'update' and 'destroy' actions.
    """
    queryset = Role.objects.all()
    permission_classes = [IsStaffOrReadOnly]


    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminRoleSerializer
        return NonAdminRoleSerializer