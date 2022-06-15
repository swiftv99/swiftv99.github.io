from rest_framework import serializers

from apps.user.models import Role


# Role model
class AdminRoleSerializer(serializers.HyperlinkedModelSerializer):
    users = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail', read_only=True)
    class Meta:
        model = Role
        fields = ['url', 'id', 'role', 'users']


class NonAdminRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['url', 'id', 'role']
