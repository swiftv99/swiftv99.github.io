from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from apps.user.models import Role, User


class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_2 = serializers.CharField(write_only=True, required=True)
    role = serializers.SlugRelatedField(slug_field='role', queryset=Role.objects.exclude(role='admin').all())

    class Meta:
        model = User
        fields = ['url', 'id', 'email', 'password', 'password_2',  'role', 'phone', 'country', 'city']
        extra_kwargs = {
            'role': {'required': True},
            'phone': {'required': True},
            'country': {'required': True},
            'city': {'required': True}
        }


    def validate(self, attrs):
        if attrs['password'] != attrs['password_2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs


    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            role=validated_data['role'],
            phone=validated_data['phone'],
            country=validated_data['country'],
            city=validated_data['city'],
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    new_password_2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'old_password', 'new_password', 'new_password_2']


    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs


    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value


    def update(self, instance, validated_data):
        user = self.context['request'].user

        if not (user.is_staff or user.pk == instance.pk):
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


# class UpdateUserSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(required=True)
#     role = serializers.SlugRelatedField(slug_field='role', read_only=True) #queryset=Role.objects.all())

#     class Meta:
#         model = User
#         fields = ['url', 'id', 'email', 'role', 'phone', 'country', 'city']
#         extra_kwargs = {
#             # 'role': {'required': True},
#             'phone': {'required': True},
#             'country': {'required': True},
#             'city': {'required': True}
#         }

#     def validate_email(self, value):
#         user = self.context['request'].user
#         if User.objects.exclude(pk=user.pk).filter(email=value).exists():
#             raise serializers.ValidationError({"email": "This email is already in use."})
#         return value


    # def update(self, instance, validated_data):
    #     user = self.context['request'].user

    #     if not (user.is_staff or user.pk == instance.pk):
    #         raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

    #     instance.email = validated_data['email']
    #     instance.role = validated_data['role']
    #     instance.phone = validated_data['phone']
    #     instance.country = validated_data['country']
    #     instance.city = validated_data['city']

    #     instance.save()
    #     return instance