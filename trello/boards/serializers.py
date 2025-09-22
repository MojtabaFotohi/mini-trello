from rest_framework import serializers
from .models import Board
from users.serializers import UserSerializer

class BoardSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Board
        fields = ['id', 'title', 'owner', 'members', 'color', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']
        
        
        
        
    