import random
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import TaskTest
from practice_test.models import Category, Theme, Question
from .serializers import (
    StartTaskTestSerializer,
    TaskQuestionSerializer,
    SubmitTaskAnswerSerializer,
    TaskTestResultSerializer,
    TaskПодсказкаSerializer
)
from user_answer.models import UserAnswer
from users.models import User
from подсказки.models import Подсказка as TaskПодсказка  # Чтобы не было конфликта имен


class StartTaskTestView(generics.CreateAPIView):
    serializer_class = StartTaskTestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category_id = serializer.validated_data['category_id']
        theme_id = serializer.validated_data.get('theme_id')

        try:
            category = Category.objects.get(pk=category_id)
            filters = {'category': category}
            if theme_id:
                filters['theme_id'] = theme_id

            questions = Question.objects.filter(**filters).order_by('?')[:20]  # 20 вопросов

            if not questions:
                return Response({"error": "Нет доступных вопросов по выбранным критериям."},
                                status=status.HTTP_400_BAD_REQUEST)

            task_test = TaskTest.objects.create(user=request.user, category=category, theme_id=theme_id)
            test_id = task_test.id

            response_data = []
            for question in questions:
                response_data.append({
                    'test_id': test_id,
                    'question_id': question.id,
                    'text': question.text,
                    'options': {
                        'A': question.option_a,
                        'B': question.option_b,
                        'C': question.option_c,
                        'D': question.option_d,
                    }
                })
                UserAnswer.objects.create(
                    user=request.user,
                    test=task_test,
                    question=question,
                    question_number=len(response_data),  # Порядковый номер вопроса
                    status='not_answered'
                )

            return Response(response_data, status=status.HTTP_201_CREATED)
        except Category.DoesNotExist:
            return Response({"error": "Указанная категория не найдена."}, status=status.HTTP_400_BAD_REQUEST)
        except Theme.DoesNotExist:
            return Response({"error": "Указанная тема не найдена."}, status=status.HTTP_400_BAD_REQUEST)


class SubmitTaskAnswerView(generics.CreateAPIView):
    serializer_class = SubmitTaskAnswerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        test_id = serializer.validated_data['test_id']
        question_id = serializer.validated_data['question_id']
        selected_answer = serializer.validated_data['selected_answer'].upper()

        try:
            task_test = TaskTest.objects.get(pk=test_id, user=request.user, end_time__isnull=True)
            question = Question.objects.get(pk=question_id)
            user_answer, created = UserAnswer.objects.get_or_create(
                user=request.user,
                test=task_test,
                question=question
            )
            user_answer.selected_answer = selected_answer

            if selected_answer == question.correct_answer:
                user_answer.is_correct = True
                user_answer.status = 'correct'
                response_message = {"message": "Молодец, ты правильно ответил"}
            else:
                user_answer.is_correct = False
                user_answer.status = 'incorrect'
                response_message = {"message": "Ответ неверный, попробуй ещё раз или воспользуйся подсказкой"}
            user_answer.save()
            return Response(response_message, status=status.HTTP_200_OK)
        except TaskTest.DoesNotExist:
            return Response({"error": "Тест не найден или уже завершен."}, status=status.HTTP_404_NOT_FOUND)
        except Question.DoesNotExist:
            return Response({"error": "Вопрос не найден."}, status=status.HTTP_404_NOT_FOUND)


class TaskTestResultsView(generics.RetrieveAPIView):
    serializer_class = TaskTestResultSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        test_id = self.request.query_params.get('test_id')
        if not test_id:
            return Response({"error": "Необходимо указать ID теста."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            task_test = TaskTest.objects.get(pk=test_id, user=request.user)
            if task_test.end_time is None:
                task_test.end_time = timezone.now()
                task_test.save()

            user_answers = UserAnswer.objects.filter(test=task_test, user=request.user)
            total_questions = user_answers.count()
            answered_questions = user_answers.exclude(selected_answer__isnull=True).count()
            correct_answers = user_answers.filter(is_correct=True).count()
            incorrect_answers = user_answers.filter(is_correct=False).count()

            start_time = task_test.start_time
            end_time = task_test.end_time
            time_taken_seconds = int((end_time - start_time).total_seconds())

            # ELO Calculation (Simplified)
            user = request.user
            initial_elo = user.elo
            expected_score = 1 / (
                    1 + 10 ** ((1000 - initial_elo) / 400))  # Предполагаемый счет против "среднего" оппонента
            actual_score = correct_answers / total_questions  # Фактический счет
            k = 30  # K-factor
            elo_change = int(k * (actual_score - expected_score))
            new_elo = initial_elo + elo_change
            User.objects.filter(id=user.id).update(elo=new_elo)  # Обновляем ELO

            results = {
                'total_questions': total_questions,
                'answered_questions': answered_questions,
                'correct_answers': correct_answers,
                'incorrect_answers': incorrect_answers,
                'time_taken': time_taken_seconds,
                'elo_change': elo_change,
                'new_elo': new_elo,
            }

            return Response(results, status=status.HTTP_200_OK)
        except TaskTest.DoesNotExist:
            return Response({"error": "Тест не найден."}, status=status.HTTP_404_NOT_FOUND)


class GetTaskHintView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TaskПодсказкаSerializer

    def get_object(self):
        question_id = self.request.query_params.get('question_id')
        if question_id:
            try:
                question = Question.objects.get(pk=question_id)
                подсказка = TaskПодсказка.objects.filter(question=question).first()
                if подсказка:
                    return подсказка
                else:
                    return None
            except Question.DoesNotExist:
                return None
        return None

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response({"message": "Подсказка для этого вопроса отсутствует."}, status=status.HTTP_204_NO_CONTENT)


class SkipTaskQuestionView(generics.UpdateAPIView):
    serializer_class = SubmitTaskAnswerSerializer  # Используем существующий сериализатор
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        test_id = serializer.validated_data['test_id']
        question_id = serializer.validated_data['question_id']

        try:
            task_test = TaskTest.objects.get(pk=test_id, user=request.user, end_time__isnull=True)
            question = Question.objects.get(pk=question_id)
            user_answer = UserAnswer.objects.get(user=request.user, test=task_test, question=question)
            user_answer.status = 'skipped'
            user_answer.save()
            return Response({"message": "Вопрос пропущен."}, status=status.HTTP_200_OK)
        except TaskTest.DoesNotExist:
            return Response({"error": "Тест не найден или уже завершен."}, status=status.HTTP_404_NOT_FOUND)
        except Question.DoesNotExist:
            return Response({"error": "Вопрос не найден."}, status=status.HTTP_404_NOT_FOUND)
        except UserAnswer.DoesNotExist:
            return Response({"error": "Ответ пользователя не найден."}, status=status.HTTP_404_NOT_FOUND)
