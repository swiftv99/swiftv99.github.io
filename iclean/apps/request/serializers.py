from rest_framework import serializers

from apps.request.models import RequestStatus, Request
from apps.service.models import Service


# RequestStatus model
class AdminRequestStatusSerializer(serializers.HyperlinkedModelSerializer):
    requests = serializers.HyperlinkedRelatedField(many=True, view_name='request-detail', read_only=True)
    class Meta:
        model = RequestStatus
        fields = ['url', 'id', 'name', 'requests']


class NonAdminRequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestStatus
        fields = ['url', 'id', 'name']


# Request model
class ReadRequestSerializer(serializers.HyperlinkedModelSerializer):
    total_price = serializers.SerializerMethodField()
    client = serializers.SlugRelatedField(slug_field='full_name', read_only=True)
    status = serializers.SlugRelatedField(slug_field='name', read_only=True)
    service = serializers.SlugRelatedField(slug_field='name', read_only=True)
    # notifications = serializers.HyperlinkedRelatedField(many=True, view_name='notification-detail', read_only=True)
    class Meta:
        model = Request
        fields = ['url', 'id', 'name', 'total_area', 'total_price', 'created_at', 'client', 'status', 'service', 'slug', 'notifications']

    def get_total_price(self, request_item:Request):
        return request_item.total_area * request_item.service.cost_of_service


class AdminCreateRequestSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(slug_field='name', queryset=RequestStatus.objects.all())
    service = serializers.SlugRelatedField(slug_field='name', queryset=Service.objects.all())
    class Meta:
        model = Request
        fields = ['url', 'id', 'name', 'total_area', 'client', 'status', 'service']


class ClientCreateRequestSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(slug_field='full_name', read_only=True)
    status = serializers.SlugRelatedField(slug_field='name', queryset=RequestStatus.objects.all())
    service = serializers.SlugRelatedField(slug_field='name', queryset=Service.objects.all())
    class Meta:
        model = Request
        fields = ['url', 'id', 'name', 'total_area', 'client', 'status', 'service']


class CompanyUpdateRequestSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(slug_field='name', queryset=RequestStatus.objects.all())
    class Meta:
        model = Request
        fields = ['url', 'id', 'name', 'total_area', 'status', 'service']
        read_only_fields = ['name', 'total_area', 'service']