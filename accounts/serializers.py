from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser 
        fields = ('username', 'email', 'password', 'password2')

def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.pop('password2')
    if password != password2:
        raise serializers.ValidationError('password do not match')
    return super().validate(attrs)
    
def create(self, validated_data):
    user = CustomUser.objects.create_user(**validated_data)
    return user
    