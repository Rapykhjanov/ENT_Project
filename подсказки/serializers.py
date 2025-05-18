from rest_framework import serializers
from .models import Подсказка

class ПодсказкаSerializer(serializers.ModelSerializer):
    class Meta:
        model = Подсказка
        fields = ('id', 'question', 'text')
        read_only_fields = ('id', 'question')
