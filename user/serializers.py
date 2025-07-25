from rest_framework import serializers
from django.contrib.auth import get_user_model

from user.models import USER_TYPE_CHOICES

User = get_user_model()

# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for view user details.
    """
    class Meta:
        model = User
        fields ='__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration with all required fields.
    """
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    user_type = serializers.ChoiceField(choices=USER_TYPE_CHOICES, required=True)
    class Meta:
        model = User
        fields ='__all__'
        

    def create(self, validated_data):
        """
         Create and return a new user with the validated data.
        """
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({'message': 'A user with this email already exists.'})
        if User.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError({'message': 'A user with this username already exists.'})
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=validated_data['user_type']
        )
        return user
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'is_superuser', 'is_staff', 'groups', 'user_permissions']