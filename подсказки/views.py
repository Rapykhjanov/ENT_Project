from rest_framework import generics, permissions
from .models import Подсказка
from .serializers import ПодсказкаSerializer

class ПодсказкаListView(generics.ListAPIView):
    queryset = Подсказка.objects.all()
    serializer_class = ПодсказкаSerializer
    permission_classes = (permissions.IsAuthenticated,)

class ПодсказкаDetailView(generics.RetrieveAPIView):
    queryset = Подсказка.objects.all()
    serializer_class = ПодсказкаSerializer
    permission_classes = (permissions.IsAuthenticated,)
