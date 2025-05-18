from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Theme, Question, PracticeTest
from .serializers import (
    CategorySerializer,
    ThemeSerializer,
    QuestionSerializer,
    StartPracticeTestSerializer,
    SubmitAnswerSerializer,
    PracticeTestResultSerializer,
    QuestionWithAnswerSerializer,
    ПодсказкаSerializer
)
from подсказки.models import Подсказка
from user_answer.models import UserAnswer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated,)


class ThemeListView(generics.ListAPIView):
    serializer_class = ThemeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        category_id = self.kwargs.get('cat_id')
        if category_id:
            return Theme.objects.filter(category_id=category_id)
        return Theme.objects.none()


class DifficultyLevelsView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, cat_id):
        return Response([choice[0] for choice in Question.DIFFICULTY_CHOICES], status=status.HTTP_200_OK)


class StartPracticeTestView(generics.CreateAPIView):
    serializer_class = StartPracticeTestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category_id = serializer.validated_data['category_id']
        difficulty = serializer.validated_data.get('difficulty')
        theme_id = serializer.validated_data.get('theme_id')

        try:
            category = Category.objects.get(pk=category_id)
            filters = {'category': category}
            if difficulty:
                filters['difficulty'] = difficulty
            if theme_id:
                filters['theme_id'] = theme_id

            questions = Question.objects.filter(**filters).order_by('?')[:20]  # Например, 20 случайных вопросов
            if not questions:
                return Response({"error": "Нет доступных вопросов по выбранным критериям."},
                                status=status.HTTP_400_BAD_REQUEST)

            practice_test = PracticeTest.objects.create(user=request.user, category=category, difficulty=difficulty,
                                                        theme_id=theme_id)
            test_id = practice_test.id
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
                    test=practice_test,
                    question=question,
                    question_number=len(response_data),  # Порядковый номер вопроса в тесте
                    status='not_answered'
                )

            return Response(response_data, status=status.HTTP_201_CREATED)
        except Category.DoesNotExist:
            return Response({"error": "Указанная категория не найдена."}, status=status.HTTP_400_BAD_REQUEST)
        except Theme.DoesNotExist:
            return Response({"error": "Указанная тема не найдена."}, status=status.HTTP_400_BAD_REQUEST)


class SubmitAnswerView(generics.CreateAPIView):
    serializer_class = SubmitAnswerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        test_id = serializer.validated_data['test_id']
        question_id = serializer.validated_data['question_id']
        selected_answer = serializer.validated_data['selected_answer'].upper()

        try:
            practice_test = PracticeTest.objects.get(pk=test_id, user=request.user, end_time__isnull=True)
            question = Question.objects.get(pk=question_id)
            user_answer, created = UserAnswer.objects.get_or_create(
                user=request.user,
                test=practice_test,
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
        except PracticeTest.DoesNotExist:
            return Response({"error": "Тест не найден или уже завершен."}, status=status.HTTP_404_NOT_FOUND)
        except Question.DoesNotExist:
            return Response({"error": "Вопрос не найден."}, status=status.HTTP_404_NOT_FOUND)


class GetHintView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ПодсказкаSerializer

    def get_object(self):
        question_id = self.request.query_params.get('question_id')
        if question_id:
            try:
                question = Question.objects.get(pk=question_id)
                подсказка = Подсказка.objects.filter(question=question).first()
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


class SkipQuestionView(generics.UpdateAPIView):
    serializer_class = SubmitAnswerSerializer  # Можно использовать существующий, главное - test_id и question_id
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        test_id = serializer.validated_data['test_id']
        question_id = serializer.validated_data['question_id']

        try:
            practice_test = PracticeTest.objects.get(pk=test_id, user=request.user, end_time__isnull=True)
            question = Question.objects.get(pk=question_id)
            user_answer = UserAnswer.objects.get(user=request.user, test=practice_test, question=question)
            user_answer.status = 'skipped'
            user_answer.save()
            return Response({"message": "Вопрос пропущен."}, status=status.HTTP_200_OK)
        except PracticeTest.DoesNotExist:
            return Response({"error": "Тест не найден или уже завершен."}, status=status.HTTP_404_NOT_FOUND)
        except Question.DoesNotExist:
            return Response({"error": "Вопрос не найден."}, status=status.HTTP_404_NOT_FOUND)
        except UserAnswer.DoesNotExist:
            return Response({"error": "Ответ пользователя не найден."}, status=status.HTTP_404_NOT_FOUND)


class PracticeTestResultsView(generics.RetrieveAPIView):
    serializer_class = PracticeTestResultSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        test_id = self.request.query_params.get('test_id')
        if not test_id:
            return Response({"error": "Необходимо указать ID теста."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            practice_test = PracticeTest.objects.get(pk=test_id, user=request.user)
            user_answers = UserAnswer.objects.filter(test=practice_test, user=request.user)
            total_questions = user_answers.count()
            answered_questions = user_answers.exclude(selected_answer__isnull=True).count()
            skipped_questions = user_answers.filter(status='skipped').count()
            correct_answers = user_answers.filter(is_correct=True).count()
            incorrect_answers = user_answers.filter(is_correct=False).count()
            score = correct_answers  # Просто количество правильных ответов для практики

            results = {
                'total_questions': total_questions,
                'answered_questions': answered_questions,
                'skipped_questions': skipped_questions,
                'correct_answers': correct_answers,
                'incorrect_answers': incorrect_answers,
                'score': score,
            }
            return Response(results, status=status.HTTP_200_OK)
        except PracticeTest.DoesNotExist:
            return Response({"error": "Тест не найден."}, status=status.HTTP_404_NOT_FOUND)
