from rest_framework import viewsets, serializers

from apps.user.models import Client
from apps.user.permissions import IsStaff, IsClient
from apps.user.serializers.client import ReadClientSerializer, CreateUpdateClientSerializer, AdminCreateClientSerializer


# Client model
class ClientViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list', 'create', 'retrieve',
    'update' and 'destroy' actions.
    """
    permission_classes = [IsStaff | IsClient]


    def get_queryset(self):
        queryset = Client.objects.select_related('user').all()
        is_staff = getattr(self.request.user, "is_staff", None)
        if not is_staff:
            queryset = queryset.filter(user=self.request.user.id)
        return queryset


    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminCreateClientSerializer
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            return CreateUpdateClientSerializer
        return ReadClientSerializer


    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            if Client.objects.filter(user=self.request.user).exists():
                raise serializers.ValidationError({"email": "This email is already in use."})
            serializer.save(user=self.request.user)
        serializer.save()