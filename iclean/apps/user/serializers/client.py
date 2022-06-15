from rest_framework import serializers

from apps.user.models import User, Client


# Client model
class ReadClientSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.SlugRelatedField(slug_field='id', read_only=True)
    # requests = serializers.HyperlinkedRelatedField(many=True, view_name='request-detail', read_only=True)
    # reviews = serializers.HyperlinkedRelatedField(many=True, view_name='review-detail', read_only=True)
    class Meta:
        model = Client
        fields = ['url', 'user', 'first_name', 'last_name', 'street', 'house_number', 
        'apartment', 'requests', 'reviews']


class CreateUpdateClientSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='id', read_only=True)
    class Meta:
        model = Client
        fields = ['url', 'user', 'first_name', 'last_name', 'street', 'house_number', 'apartment']


class AdminCreateClientSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='id', queryset=User.objects.all())
    class Meta:
        model = Client
        fields = ['url', 'user', 'first_name', 'last_name', 'street', 'house_number', 'apartment']

    def validate_user(self, value):
        user_id = self.context['request'].data['user']
        if Client.objects.filter(user_id__email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value