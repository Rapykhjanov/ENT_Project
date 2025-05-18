from django.db import models
from practice_test.models import Question # Импортируем модель Question

class Подсказка(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='подсказка')
    text = models.TextField()

    def __str__(self):
        return f"Подсказка к вопросу: {self.question.text[:50]}..."
