from rest_framework import serializers
from .models import Board

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'owner', 'color', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']