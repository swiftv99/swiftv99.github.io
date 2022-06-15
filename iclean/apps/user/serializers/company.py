from rest_framework import serializers

from apps.user.models import User, Company


# Company model
class ReadCompanySerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.SlugRelatedField(slug_field='id', read_only=True)
    # services = serializers.HyperlinkedRelatedField(many=True, view_name='service-detail', read_only=True)
    # notifications = serializers.HyperlinkedRelatedField(many=True, view_name='notification-detail', read_only=True)
    class Meta:
        model = Company
        fields = ['url', 'user', 'name', 'services', 'notifications']


class CreateUpdateCompanySerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='id', read_only=True)
    class Meta:
        model = Company
        fields = ['url', 'user', 'name' ]


class AdminCreateCompanySerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='id', queryset=User.objects.all())
    class Meta:
        model = Company
        fields = ['url', 'user', 'name' ]

    def validate_user(self, value):
        user_id = self.context['request'].data['user']
        if Company.objects.filter(user_id__email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value