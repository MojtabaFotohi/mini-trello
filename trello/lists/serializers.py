from rest_framework import serializers
from .models import List, Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'list', 'due_date', 'order', 'created_at', 'updated_at']
        read_only_fields = ['list', 'created_at', 'updated_at']

class ListSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = List
        fields = ['id', 'title', 'board', 'tasks', 'created_at', 'updated_at']
        read_only_fields = ['board', 'created_at', 'updated_at']