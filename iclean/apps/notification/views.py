from rest_framework import viewsets
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.notification.filters import NotificationFilter
from apps.notification.models import Notification
from apps.notification.permissions import IsStaff, IsSender
from apps.notification.serializers import ReadNotificationSerializer, AdminCreateNotificationSerializer, \
            ClientCreateNotificationSerializer, CompanyCreateNotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list', 'create', 'retrieve',
    'update' and 'destroy' actions.
    """
    queryset = Notification.objects.select_related('request', 'company').all()
    serializer_class = ReadNotificationSerializer
    permission_classes = [IsStaff | IsSender]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = NotificationFilter
    search_fields = ['name', 'details']
    ordering_fields = ['created_at']


    def get_queryset(self):
        queryset = Notification.objects.select_related('sender', 'request', 'company').all()
        is_staff = getattr(self.request.user, "is_staff", None)
        if not is_staff:
            queryset = queryset.filter(Q(request__client=self.request.user.id) | Q(company=self.request.user.id))
        return queryset


    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            if self.request.user.is_staff:
                return AdminCreateNotificationSerializer
            if self.request.user.role.role == "client":
                return ClientCreateNotificationSerializer
            return CompanyCreateNotificationSerializer
        return ReadNotificationSerializer


    def perform_create(self, serializer):
        if self.request.user.role.role == 'client':
            serializer.save(sender=self.request.user)
        elif self.request.user.role.role == 'company':
            serializer.save(sender=self.request.user, company=self.request.user.companys)
        serializer.save()