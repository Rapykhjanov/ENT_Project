from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)
    level = models.IntegerField(default=1)
    elo = models.IntegerField(default=600)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="ent_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="ent_user_set",
        related_query_name="user",
    )

    def __str__(self):
        return self.username

class Level(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    bonus = models.TextField(blank=True, null=True)
    theory_file = models.FileField(upload_to='levels/theory/', blank=True, null=True)

    def __str__(self):
        return self.name
