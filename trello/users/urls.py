from django.urls import path
from .views import RegisterView, ProfileView, TestTranslationView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('test-translation/', TestTranslationView.as_view(), name='test-translation'),
]