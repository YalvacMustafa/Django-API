from django.urls import path, include
from .views import TakimPersonellerAPIView, TakimView

urlpatterns = [
    path('<int:pk>/personeller/', TakimPersonellerAPIView.as_view(), name='takim-personeller'),
    path('takimlar/', TakimView.as_view(), name='takim-list-create')
]