from rest_framework import serializers

from apps.review.models import Review
from apps.service.models import Service


class ReadReviewSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(slug_field='full_name', read_only=True)
    service = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = Review
        fields = ['url', 'id', 'comment', 'rating', 'created_at', 'client', 'service', 'slug']


class AdminCreateReviewSerializer(serializers.ModelSerializer):
    service = serializers.SlugRelatedField(slug_field='name', queryset=Service.objects.all())
    class Meta:
        model = Review
        fields = ['url', 'id', 'comment', 'rating', 'client', 'service']


class ClientCreateReviewSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(slug_field='full_name', read_only=True)
    service = serializers.SlugRelatedField(slug_field='name', queryset=Service.objects.all())
    class Meta:
        model = Review
        fields = ['url', 'id', 'comment', 'rating', 'client', 'service']