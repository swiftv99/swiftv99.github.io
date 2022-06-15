from django_filters.rest_framework import FilterSet

from apps.request.models import Request


class RequestFilter(FilterSet):
    class Meta:
        model = Request
        fields = {
            'client': ['exact'],
            'service': ['exact'],
            'status': ['exact'],
        }