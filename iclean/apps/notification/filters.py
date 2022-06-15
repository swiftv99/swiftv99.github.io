from django_filters.rest_framework import FilterSet

from apps.notification.models import Notification


class NotificationFilter(FilterSet):
    class Meta:
        model = Notification
        fields = {
            'request': ['exact'],
            'company': ['exact'],
        }