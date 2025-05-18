from rest_framework import serializers
from .models import Category, Theme, Question, PracticeTest
from подсказки.models import Подсказка

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ('id', 'name')

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'text', 'option_a', 'option_b', 'option_c', 'option_d')

class QuestionWithAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer')

class ПодсказкаSerializer(serializers.ModelSerializer):
    class Meta:
        model = Подсказка
        fields = ('text',)

class StartPracticeTestSerializer(serializers.Serializer):
    category_id = serializers.IntegerField(required=True)
    difficulty = serializers.ChoiceField(choices=Question.DIFFICULTY_CHOICES, required=False)
    theme_id = serializers.IntegerField(required=False)

class SubmitAnswerSerializer(serializers.Serializer):
    test_id = serializers.IntegerField(required=True)
    question_id = serializers.IntegerField(required=True)
    selected_answer = serializers.CharField(max_length=1, required=True)

class PracticeTestResultSerializer(serializers.Serializer):
    total_questions = serializers.IntegerField()
    answered_questions = serializers.IntegerField()
    skipped_questions = serializers.IntegerField()
    correct_answers = serializers.IntegerField()
    incorrect_answers = serializers.IntegerField()
    score = serializers.IntegerField()
