from .models import Takim
from .serializers import TakimSerializer
from personel.serializers import PersonelSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .permissions import SuperAdminPermission
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi

class TakimPersonellerAPIView(ListModelMixin, GenericAPIView):
    serializer_class = PersonelSerializer
    queryset = Takim.objects.all() 

    def get_queryset(self, *args, **kwargs):
        takim = get_object_or_404(Takim, pk=self.kwargs.get('pk'))
        return takim.personeller.all()
    
    @swagger_auto_schema(
        operation_summary='Takıma ait personeller',
        operation_description="Bir takımın personellerini döndürür.",
        responses={200: PersonelSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TakimView(APIView):

    @swagger_auto_schema(
        operation_summary="Takımları listele",
        operation_description="Tüm takımları listeler.",
        responses={
            200: TakimSerializer(many=True),
            400: "Bad Request"
        }
    )
    def get(self, request, *args, **kwargs):
        takimlar = Takim.objects.all()
        serializer = TakimSerializer(takimlar, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_summary="Takım oluştur.",
        operation_description="Yeni bir takım oluşturur. Sadece Süper Admin yetkisine sahip kullanıcılar erişebilir.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "isim": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Takım adı",
                    example="Kanat Takımı"
                ),
                "aciklama": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Takım açıklaması"
                ),
            },
            required=["isim"]
        ),
        responses={
            201: openapi.Response(
                description="Başarıyla oluşturuldu",
                examples={
                    "application/json": {
                        "id": 1,
                        "isim": "Kanat Takımı"
                    }
                }
            ),
            400: "Bad Request",
            403: "Permission Denied"
        }
    )
    def post(self, request, *args, **kwargs):
        self.permission_classes = [SuperAdminPermission]
        self.check_permissions(request)
        serializer = TakimSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

