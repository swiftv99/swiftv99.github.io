from rest_framework import viewsets
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.request.filters import RequestFilter
from apps.request.models import Request, RequestStatus
from apps.request.permissions import IsStaffOrReadOnly, IsStaff, IsClient, IsCompany 
from apps.request.serializers import AdminRequestStatusSerializer, NonAdminRequestStatusSerializer, \
        ReadRequestSerializer, AdminCreateRequestSerializer, ClientCreateRequestSerializer, CompanyUpdateRequestSerializer


# RequestStatus model
class RequestStatusViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list', 'create', 'retrieve',
    'update' and 'destroy' actions.
    """
    queryset = RequestStatus.objects.all()
    permission_classes = [IsStaffOrReadOnly]
    

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminRequestStatusSerializer
        return NonAdminRequestStatusSerializer



# Request model
class RequestViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list', 'create', 'retrieve',
    'update' and 'destroy' actions.
    """
    queryset = Request.objects.select_related('client', 'status', 'service').all()
    serializer_class = ReadRequestSerializer
    permission_classes = [IsStaff | IsClient | IsCompany]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = RequestFilter
    search_fields = ['name', 'service__name']
    ordering_fields = ['total_area', 'created_at']

   
    def get_queryset(self):
        queryset = Request.objects.select_related('client', 'status', 'service').all()
        is_staff = getattr(self.request.user, "is_staff", None)
        if not is_staff:
            queryset = queryset.filter(Q(client=self.request.user.id) | Q(service__company=self.request.user.id))
        return queryset


    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            if self.request.user.is_staff:
                return AdminCreateRequestSerializer
            elif self.request.user.role.role == 'client':
                return ClientCreateRequestSerializer
            return CompanyUpdateRequestSerializer
        return ReadRequestSerializer
    

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            serializer.save(client=self.request.user.clients)
        serializer.save()