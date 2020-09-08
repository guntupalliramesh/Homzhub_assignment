from rest_framework import serializers
from .models import UserRequest

class UserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRequest
        fields = '__all__'
