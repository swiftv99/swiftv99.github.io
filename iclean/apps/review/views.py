from rest_framework import viewsets
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.review.filters import ReviewFilter
from apps.review.models import Review
from apps.review.permissions import IsStaff, IsClient, IsCompany 
from apps.review.serializers import ReadReviewSerializer, AdminCreateReviewSerializer, ClientCreateReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list', 'create', 'retrieve',
    'update' and 'destroy' actions.
    """
    # queryset = Review.objects.select_related('client', 'company').all()
    serializer_class = ReadReviewSerializer
    permission_classes = [IsStaff | IsClient | IsCompany]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ReviewFilter
    search_fields = ['comment']
    ordering_fields = ['rating', 'created_at']


    def get_queryset(self):
        queryset = Review.objects.select_related('client', 'service').all()
        is_staff = getattr(self.request.user, "is_staff", None)
        if not is_staff:
            queryset = queryset.filter(Q(client=self.request.user.id) | Q(service__company=self.request.user.id))
        return queryset
    

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            if self.request.user.is_staff:
                return AdminCreateReviewSerializer
            return ClientCreateReviewSerializer
        return ReadReviewSerializer
    

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            serializer.save(client=self.request.user.clients)
        serializer.save()