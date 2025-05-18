from rest_framework import serializers
from .models import UserAnswer

class UserAnswerSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.text', read_only=True) # Добавляем поле для текста вопроса

    class Meta:
        model = UserAnswer
        fields = ('id', 'question', 'question_number', 'selected_answer', 'is_correct', 'status', 'question_text') # Добавили 'question_text'
        read_only_fields = ('id', 'is_correct', 'status', 'question_text') # 'question_text' тоже только для чтения

class UserAnswerDetailSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.text', read_only=True)

    class Meta:
        model = UserAnswer
        fields = ('id', 'user', 'test', 'question', 'question_number', 'selected_answer', 'is_correct', 'status', 'question_text')
        read_only_fields = ('id', 'user', 'test', 'question', 'question_number', 'is_correct', 'status', 'question_text')
