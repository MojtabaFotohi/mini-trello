from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import List, Task
from .serializers import ListSerializer, TaskSerializer
from boards.models import Board

class ListListCreateView(generics.ListCreateAPIView):
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        board_id = self.kwargs.get('board_id')
        return List.objects.filter(board__id=board_id, board__owner=self.request.user)

    def perform_create(self, serializer):
        board_id = self.kwargs.get('board_id')
        board = Board.objects.get(id=board_id, owner=self.request.user)
        serializer.save(board=board)

class ListDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        board_id = self.kwargs.get('board_id')
        return List.objects.filter(board__id=board_id, board__owner=self.request.user)

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        list_id = self.kwargs.get('list_id')
        return Task.objects.filter(list__id=list_id, list__board__owner=self.request.user)

    def perform_create(self, serializer):
        list_id = self.kwargs.get('list_id')
        list_obj = List.objects.get(id=list_id, board__owner=self.request.user)
        serializer.save(list=list_obj)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        list_id = self.kwargs.get('list_id')
        return Task.objects.filter(list__id=list_id, list__board__owner=self.request.user)

class TaskMoveView(generics.UpdateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(list__board__owner=self.request.user)

    def perform_update(self, serializer):
        new_list_id = self.request.data.get('list_id')
        new_order = self.request.data.get('order')
        if new_list_id:
            new_list = List.objects.get(id=new_list_id, board__owner=self.request.user)
            serializer.save(list=new_list)
        if new_order is not None:
            serializer.save(order=new_order)