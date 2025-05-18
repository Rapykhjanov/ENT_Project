from rest_framework import serializers
from .models import TaskTest
from practice_test.models import Question
from подсказки.models import Подсказка as TaskПодсказка # Чтобы не было конфликта имен

class StartTaskTestSerializer(serializers.Serializer):
    category_id = serializers.IntegerField(required=True)
    theme_id = serializers.IntegerField(required=False)

class TaskQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'text', 'option_a', 'option_b', 'option_c', 'option_d')

class SubmitTaskAnswerSerializer(serializers.Serializer):
    test_id = serializers.IntegerField(required=True)
    question_id = serializers.IntegerField(required=True)
    selected_answer = serializers.CharField(max_length=1, required=True)

class TaskTestResultSerializer(serializers.Serializer):
    total_questions = serializers.IntegerField()
    answered_questions = serializers.IntegerField()
    correct_answers = serializers.IntegerField()
    incorrect_answers = serializers.IntegerField()
    time_taken = serializers.IntegerField() # В секундах
    elo_change = serializers.IntegerField()
    new_elo = serializers.IntegerField()

class TaskПодсказкаSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskПодсказка
        fields = ('text',)
