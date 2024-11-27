from django.urls import path
from .views import ParcaListCreateView, ParcaDeleteView

urlpatterns = [
    path('create-list/', ParcaListCreateView.as_view(), name='parca-list-create'),
    path('<int:pk>/delete/', ParcaDeleteView.as_view(), name='parca-delete'),
]