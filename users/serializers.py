from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'image', 'dob', 'date_joined', 'is_verified']


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(**attrs)
        if user and user.is_active and user.is_verified:
            return user
        if user and user.is_active and not user.is_verified:
            raise serializers.ValidationError('Account not active. Please visit conmeter.com to activate.')
        raise serializers.ValidationError('Wrong Credentials')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'password', 'name', 'dob']

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['email'],
            validated_data['password'],
            **{"name": validated_data['name'], "dob":  validated_data['dob'], "phone": validated_data['phone']}
        )
        return user
