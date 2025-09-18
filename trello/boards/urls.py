from django.urls import path
from .views import BoardListCreateView, BoardDetailView

urlpatterns = [
        path('', BoardListCreateView.as_view(), name='board-list-create'),
        path('<int:pk>/', BoardDetailView.as_view(), name='board-detail'),
]