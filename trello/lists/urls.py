from django.urls import path
from .views import ListListCreateView, ListDetailView, TaskListCreateView, TaskDetailView, TaskMoveView

urlpatterns = [
    path('boards/<int:board_id>/lists/', ListListCreateView.as_view(), name='list-list-create'),
    path('boards/<int:board_id>/lists/<int:pk>/', ListDetailView.as_view(), name='list-detail'),
    path('lists/<int:list_id>/tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('lists/<int:list_id>/tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/move/', TaskMoveView.as_view(), name='task-move'),
]