from django.urls import path
from .views import InvitationListCreateView, InvitationAcceptView, InvitationRejectView

urlpatterns = [
    path('', InvitationListCreateView.as_view(), name='invitation-list-create'),
    path('<int:pk>/accept/', InvitationAcceptView.as_view(), name='invitation-accept'),
    path('<int:pk>/reject/', InvitationRejectView.as_view(), name='invitation-reject'),
]