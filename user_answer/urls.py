from django.urls import path
from .views import UserAnswerListView, UserAnswerDetailView

urlpatterns = [
    path('', UserAnswerListView.as_view(), name='user-answers'),
    path('<int:test_id>/', UserAnswerDetailView.as_view(), name='user-answers-by-test'),
]
