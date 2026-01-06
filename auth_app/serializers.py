from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['id', 'username', 'email', 'phone_number', 'town', 'is_donor']
        fields = ['id', 'username', 'phone_number', 'town', 'email', 'is_donor']
        read_only_fields = ['id', 'is_donor']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return user


