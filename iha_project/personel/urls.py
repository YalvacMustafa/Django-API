from django.urls import path
from .views import  PersonelDetailView

urlpatterns = [
    path('<int:pk>/', PersonelDetailView.as_view(), name='personel-detail'),
]
