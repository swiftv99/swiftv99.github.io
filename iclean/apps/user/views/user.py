from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from apps.user.filters import UserFilter
from apps.user.models import User
from apps.user.permissions import IsStaff, IsNotStaff
from apps.user.serializers.user import ReadUserSerializer, AdminCreateUserSerializer, UpdateUserSerializer


# User model 
class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list', 'create', 'retrieve',
    'update' and 'destroy' actions.
    """
    permission_classes = [IsStaff | IsNotStaff]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = UserFilter
    ordering_fields = ['id']


    def get_queryset(self):
        queryset = User.objects.select_related('role').all()
        is_staff = getattr(self.request.user, "is_staff", None)
        if not is_staff:
            queryset = queryset.filter(id=self.request.user.id)
        return queryset


    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return UpdateUserSerializer
        elif self.action in ["create", "destroy"]:
            return AdminCreateUserSerializer
        return ReadUserSerializer