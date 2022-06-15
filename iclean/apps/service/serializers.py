from rest_framework import serializers

from apps.service.models import Service


class ReadServiceSerializer(serializers.HyperlinkedModelSerializer):
    company = serializers.SlugRelatedField(slug_field='name', read_only=True)
    # requests = serializers.HyperlinkedRelatedField(many=True, view_name='request-detail', read_only=True)
    class Meta:
        model = Service
        fields = ['url', 'id', 'name', 'type_of_service', 'cost_of_service', 'created_at', 'company', 'slug', 'requests']


class AdminCreateServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['url', 'id', 'name', 'type_of_service', 'cost_of_service', 'company']


class CompanyCreateServiceSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = Service
        fields = ['url', 'id', 'name', 'type_of_service', 'cost_of_service', 'company']