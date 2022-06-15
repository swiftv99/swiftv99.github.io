from rest_framework import serializers

from apps.user.models import Role, User


# User model
class ReadUserSerializer(serializers.ModelSerializer):
    role = serializers.SlugRelatedField(slug_field='role', read_only=True)
    class Meta:
        model = User
        fields = ['url', 'id', 'email', 'role', 'phone', 'country', 'city', 'is_staff', 'is_active']


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    role = serializers.SlugRelatedField(slug_field='role', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'email', 'role', 'phone', 'country', 'city']
        extra_kwargs = {
            'phone': {'required': True},
            'country': {'required': True},
            'city': {'required': True}
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value


class AdminCreateUserSerializer(serializers.ModelSerializer):
    role = serializers.SlugRelatedField(slug_field='role', queryset=Role.objects.all())
    class Meta:
        model = User
        fields = ['url', 'id', 'email', 'role', 'phone', 'country', 'city', 'is_staff', 'is_active']


# class NonAdminCreateUserSerializer(serializers.ModelSerializer):
#     role = serializers.SlugRelatedField(slug_field='role', read_only=True)
#     class Meta:
#         model = User
#         fields = ['url', 'id', 'email', 'role', 'phone', 'country', 'city', 'is_staff', 'is_active']
#         read_only_fields = ['email', 'is_staff', 'is_active']
