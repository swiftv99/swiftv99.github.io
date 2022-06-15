from django_filters.rest_framework import FilterSet

from apps.service.models import Service


class ServiceFilter(FilterSet):
    class Meta:
        model = Service
        fields = {
            'company': ['exact'],
            'cost_of_service': ['gte', 'lte'],
        }