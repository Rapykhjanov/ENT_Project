from django.contrib import admin
from .models import Category, Theme, Question, PracticeTest

admin.site.register(Category)
admin.site.register(Theme)
admin.site.register(Question)
admin.site.register(PracticeTest)
