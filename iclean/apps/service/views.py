from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.service.filters import ServiceFilter
from apps.service.models import Service
from apps.service.permissions import IsStaff, IsClient, IsCompany 
from apps.service.serializers import ReadServiceSerializer, AdminCreateServiceSerializer, CompanyCreateServiceSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list', 'create', 'retrieve',
    'update' and 'destroy' actions.
    """
    permission_classes = [IsStaff | IsClient | IsCompany]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ServiceFilter
    search_fields = ['name', 'type_of_service']
    ordering_fields = ['cost_of_service', 'created_at']


    def get_queryset(self):
        queryset = Service.objects.select_related('company').all()
        company = getattr(self.request.user, "companys", None)
        if company is not None:
            queryset = queryset.filter(company=company.user.id)
        return queryset


    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            if self.request.user.is_staff:
                return AdminCreateServiceSerializer
            return CompanyCreateServiceSerializer
        return ReadServiceSerializer
    

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            serializer.save(company=self.request.user.companys)
        serializer.save()