from rest_framework import serializers
from rest_framework_simplejwt.serializers import (TokenObtainPairSerializer)
from .models import User

class POSLoginSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add the user's POS role to the JWT.
        token["role"] = user.role
        token["username"] = user.username

        return token

class UsezrSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","username","email","first_name","last_name","role")
        read_only_fields = fields