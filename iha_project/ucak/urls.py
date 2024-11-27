from django.urls import path
from .views import UcakListCreateView, MontajView

urlpatterns = [
    path('list/', UcakListCreateView.as_view(), name='ucak-list'),
    path('montaj/<int:ucak_id>/', MontajView.as_view(), name='ucak-montaj'),
]