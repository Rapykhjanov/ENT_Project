from django.urls import path
from .views import (
    UserRegistrationView,
    UserProfileView,
    LevelListView,
    LevelTheoryView,
    CustomTokenObtainPairView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('levels/', LevelListView.as_view(), name='level-list'),
    path('levels/<int:pk>/theory/', LevelTheoryView.as_view(), name='level-theory'),
]
