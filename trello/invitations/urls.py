from django.urls import path
from .views import InvitationListCreateView, InvitationAcceptView

urlpatterns = [
    path('', InvitationListCreateView.as_view(), name='invitation-list-create'),
    path('<int:pk>/accept/', InvitationAcceptView.as_view(), name='invitation-accept'),
]