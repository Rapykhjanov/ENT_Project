from django.db import models
from practice_test.models import Category, Theme, Question

class TaskTest(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Рейтинговый тест {self.user.username} ({self.start_time})"
