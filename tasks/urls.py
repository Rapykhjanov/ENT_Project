from django.urls import path
from .views import (
    StartTaskTestView,
    SubmitTaskAnswerView,
    TaskTestResultsView,
    GetTaskHintView,
    SkipTaskQuestionView,
)

urlpatterns = [
    path('start/', StartTaskTestView.as_view(), name='task-start'),
    path('submit-answer/', SubmitTaskAnswerView.as_view(), name='task-submit-answer'),
    path('results/', TaskTestResultsView.as_view(), name='task-results'),
    path('hint/', GetTaskHintView.as_view(), name='task-hint'),
    path('skip/', SkipTaskQuestionView.as_view(), name='task-skip'),
]
