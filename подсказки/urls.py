from django.urls import path
from .views import ПодсказкаListView, ПодсказкаDetailView

urlpatterns = [
    path('', ПодсказкаListView.as_view(), name='подсказки-list'),
    path('<int:pk>/', ПодсказкаDetailView.as_view(), name='подсказка-detail'),
]
