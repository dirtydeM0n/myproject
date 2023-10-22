from rest_framework import serializers
from .models import UserLogin

class UserLoginSerializer(serializers.Serializer):
    class Meta:
        model = UserLogin
        fields = ('username', 'password', 'email')