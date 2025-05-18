from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Theme(models.Model):
    category = models.ForeignKey(Category, related_name='themes', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('category', 'name')

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Легкий'),
        ('medium', 'Средний'),
        ('hard', 'Сложный'),
    ]
    category = models.ForeignKey(Category, related_name='questions', on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')

    def __str__(self):
        return self.text[:50] + '...'

class PracticeTest(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    difficulty = models.CharField(max_length=10, choices=Question.DIFFICULTY_CHOICES, blank=True, null=True)
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Тест {self.user.username} ({self.start_time})"
