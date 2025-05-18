from django.urls import path
from .views import (
    CategoryListView,
    ThemeListView,
    DifficultyLevelsView,
    StartPracticeTestView,
    SubmitAnswerView,
    PracticeTestResultsView,
    GetHintView,
    SkipQuestionView,
)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='practice-categories'),
    path('<int:cat_id>/levels/', DifficultyLevelsView.as_view(), name='practice-levels'),
    path('<int:cat_id>/<str:lvl>/themes/', ThemeListView.as_view(), name='practice-themes'),
    path('start/', StartPracticeTestView.as_view(), name='practice-start'),
    path('submit-answer/', SubmitAnswerView.as_view(), name='practice-submit-answer'),
    path('results/', PracticeTestResultsView.as_view(), name='practice-results'),
    path('hint/', GetHintView.as_view(), name='practice-hint'),
    path('skip/', SkipQuestionView.as_view(), name='practice-skip'),
]
