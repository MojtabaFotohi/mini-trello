from django.urls import path
from .views import InvitationListCreateView

urlpatterns = [
    path('', InvitationListCreateView.as_view(), name='invitation-list-create'),
]