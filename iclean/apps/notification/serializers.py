from rest_framework import serializers

from apps.notification.models import Notification
from apps.request.models import Request
from apps.user.models import User, Company


class ReadNotificationSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(slug_field='email', read_only=True)
    request = serializers.SlugRelatedField(slug_field='name', read_only=True)
    company = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = Notification
        fields = ['url', 'id', 'name', 'details', 'sender', 'created_at', 'request', 'company', 'slug']


class AdminCreateNotificationSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())
    request = serializers.SlugRelatedField(slug_field='name', queryset=Request.objects.all())
    company = serializers.SlugRelatedField(slug_field='name', queryset=Company.objects.all())
    class Meta:
        model = Notification
        fields = ['url', 'id', 'name', 'details', 'sender', 'request', 'company']


class ClientCreateNotificationSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(slug_field='email', read_only=True)
    request = serializers.SlugRelatedField(slug_field='name', queryset=Request.objects.all())
    company = serializers.SlugRelatedField(slug_field='name', queryset=Company.objects.all())
    class Meta:
        model = Notification
        fields = ['url', 'id', 'name', 'details', 'sender', 'request', 'company']


class CompanyCreateNotificationSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(slug_field='email', read_only=True)
    request = serializers.SlugRelatedField(slug_field='name', queryset=Request.objects.all())
    company = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = Notification
        fields = ['url', 'id', 'name', 'details', 'sender', 'request', 'company']