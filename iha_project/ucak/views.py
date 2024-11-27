from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Ucak
from .serializers import UcakSerializer
from parca.models import Parca
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class UcakListCreateView(APIView):
    @swagger_auto_schema(
        operation_summary="Uçakları Listele",
        operation_description="Mevcut tüm uçakları listeler.",
        responses={
            200: openapi.Response(
                description="Başarılı işlem",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                            "isim": openapi.Schema(type=openapi.TYPE_STRING, example="AKINCI"),
                            "montaj_sayisi": openapi.Schema(type=openapi.TYPE_INTEGER, example=5),
                        },
                    ),
                ),
            )
        },
    )
    def get(self, request, *args, **kwargs):

        ucaklar = Ucak.objects.all()
        serializer = UcakSerializer(ucaklar, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    


class MontajView(APIView):
    @swagger_auto_schema(
        operation_summary="Uçağı monte et",
        operation_description="Montaj takımı tarafından bir uçağın parçalarını kullanarak montaj işlemini gerçekleştirir.",
        manual_parameters=[
            openapi.Parameter(
                "ucak_id",
                openapi.IN_PATH,
                description="Montajı yapılacak uçağın ID'si",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Başarılı montaj",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "success": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="AKINCI başarıyla monte edildi."
                        ),
                        "kullanilan_parcalar": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                            example=["kanat", "gövde", "kuyruk", "aviyonik"]
                        ),
                        "montaj_sayisi": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            example=1
                        ),
                    },
                ),
            ),
            400: openapi.Response(
                description="Eksik parçalar nedeniyle hata",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Eksik parçalar var."
                        ),
                        "eksik_parcalar": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(type=openapi.TYPE_STRING)
                            ),
                            example=[["kanat", "AKINCI"]],
                        ),
                    },
                ),
            ),
            403: openapi.Response(
                description="Yetkisiz erişim",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Kullanıcının bir takımı yok."
                        ),
                    },
                ),
            ),
            404: openapi.Response(
                description="Uçak bulunamadı",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Sadece AKINCI, KIZILELMA, TBA2 ve TBA3 montaj edilebilir."
                        ),
                    },
                ),
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        if not hasattr(user, 'personel') or not user.personel.takim:
            return Response({'error': 'Kullanıcının bir takımı yok.'}, status=status.HTTP_403_FORBIDDEN)

        kullanici_takimi = user.personel.takim
        if kullanici_takimi.isim.lower() != 'montaj':
            return Response({'error': 'Sadece Montaj Takımı montaj işlemi yapabilir.'}, status=status.HTTP_403_FORBIDDEN)

        ucak_id = kwargs.get('ucak_id')
        try:
            ucak = Ucak.objects.get(id=ucak_id)
        except Ucak.DoesNotExist:
            return Response({"error": "Sadece AKINCI, KIZILELMA, TBA2 ve TBA3 montaj edilebilir."}, status=status.HTTP_404_NOT_FOUND)

        # Gerekli tüm parçalar
        gerekli_parcalar = ["kanat", "gövde", "kuyruk", "aviyonik"]

        # Parçaları kontrol et
        eksik_parcalar = []
        kullanilan_parcalar = []
        for parca_adi in gerekli_parcalar:
            parca = Parca.objects.filter(
                isim__icontains=parca_adi,
                ucak=ucak,
                stok__gt=0
            ).first()
            if not parca:
                eksik_parcalar.append((parca_adi, ucak.isim))
            else:
                kullanilan_parcalar.append(parca)

        if eksik_parcalar:
            return Response({
                "error": "Eksik parçalar var.",
                "eksik_parcalar": eksik_parcalar
            }, status=status.HTTP_400_BAD_REQUEST)

        # Parçalar mevcut, stokları düş ve montajı tamamla
        for parca in kullanilan_parcalar:
            parca.stok -= 1
            parca.save()

        # Uçağın montaj sayısını artır
        ucak.montaj_sayisi += 1
        ucak.save()

        return Response({
            "success": f"{ucak.isim} başarıyla monte edildi.",
            "kullanilan_parcalar": [parca.isim for parca in kullanilan_parcalar],
            "montaj_sayisi": ucak.montaj_sayisi
        }, status=status.HTTP_200_OK)

