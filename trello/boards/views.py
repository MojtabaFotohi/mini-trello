from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import Board
from .serializers import BoardSerializer
from django.db.models import Q


class BoardListCreateView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        max_boards = 5  # limit N
        if Board.objects.filter(owner=self.request.user).count() >= max_boards:
            raise ValidationError(f"Cannot create more than {max_boards} boards.")
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Board.objects.filter(Q(owner=self.request.user) | Q(members=self.request.user))

class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Board.objects.filter(Q(owner=self.request.user) | Q(members=self.request.user))
    
    
    
    
    
    
    
    
    
    
    
    
    