from django.db import models
from practice_test.models import Question

class UserAnswer(models.Model):
    STATUS_CHOICES = [
        ('not_answered', 'Не отвечено'),
        ('correct', 'Правильно'),
        ('incorrect', 'Неправильно'),
        ('skipped', 'Пропущено'),
    ]
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    test = models.ForeignKey('practice_test.PracticeTest', on_delete=models.CASCADE) # Или на tasks.TaskTest, в зависимости от того, где используется
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    question_number = models.PositiveIntegerField() # Порядковый номер вопроса в тесте
    selected_answer = models.CharField(max_length=1, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='not_answered')

    class Meta:
        unique_together = ('test', 'question') # Чтобы не было дублирования ответов на один и тот же вопрос в рамках теста

    def __str__(self):
        return f"Ответ {self.user.username} на вопрос {self.question_number} ({self.question.text[:20]}...) - {self.status}"
