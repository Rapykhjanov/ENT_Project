from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import UserAnswer
from .serializers import UserAnswerSerializer, UserAnswerDetailSerializer
from practice_test.models import PracticeTest # Импортируем PracticeTest
from tasks.models import TaskTest # Импортируем TaskTest

class UserAnswerListView(generics.ListAPIView):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return UserAnswer.objects.filter(user=self.request.user)

class UserAnswerDetailView(generics.ListAPIView):
    serializer_class = UserAnswerDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        test_id = self.kwargs.get('test_id')
        # Пытаемся получить ответы для PracticeTest и TaskTest
        practice_test = PracticeTest.objects.filter(id=test_id, user=self.request.user).first()
        task_test = TaskTest.objects.filter(id=test_id, user=self.request.user).first()

        if practice_test:
            return UserAnswer.objects.filter(test=practice_test, user=self.request.user)
        elif task_test:
            return UserAnswer.objects.filter(test=task_test, user=self.request.user)
        else:
            return UserAnswer.objects.none() # Возвращаем пустой queryset, если тест не найден
