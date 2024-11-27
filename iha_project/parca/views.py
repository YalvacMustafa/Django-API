from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.exceptions import PermissionDenied
from .models import Parca
from .serializers import ParcaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ParcaListCreateView(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Parca.objects.all()
    serializer_class = ParcaSerializer

    def get_queryset(self):
        user = self.request.user

        if not hasattr(user, 'personel') or not user.personel.takim:
            return Parca.objects.none()

        return self.queryset.filter(takim=user.personel.takim)

    def perform_create(self, serializer):
        user = self.request.user

        if not hasattr(user, 'personel') or not user.personel.takim:
            raise PermissionDenied('Kullanıcının bir takımı yok.')

        serializer.save(takim=user.personel.takim)

    @swagger_auto_schema(
        operation_summary='Takıma ait parçalar',
        operation_description='Takıma ait tüm parçaları listele.',
        responses={200: openapi.Response('Başarılı', ParcaSerializer(many=True))}
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Yeni Parça',
        operation_description='Yeni bir parça oluştur.',
        request_body=ParcaSerializer,
        responses={
            201: openapi.Response('Başarıyla oluşturuldu.', ParcaSerializer),
            403: 'Kullanıcının bir takımı yok.',
        }
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ParcaDeleteView(APIView):

    @swagger_auto_schema(
        operation_summary="Parça Silme veya Stok Azaltma",
        operation_description=(
            "Bir parçayı takım stoklarından tamamen silmek veya stok miktarını azaltmak için kullanılır. "
            "Kullanıcı sadece takımına ait parçalar üzerinde işlem yapabilir."
        ),
        manual_parameters=[
            openapi.Parameter(
                name="pk",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Silmek veya stoktan azaltmak istediğiniz parçanın ID'si",
                required=True,
            ),
            openapi.Parameter(
                name="stok",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Stoktan azaltmak istediğiniz miktar (Varsayılan: 1)",
                required=True,
    ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "stok": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Stoktan azaltmak istediğiniz miktar (Varsayılan: 1)"
                ),
            },
            required=[],
            description="Stok azaltmak için isteğe bağlı bir sayı değeri gönderin.",
        ),
        responses={
            200: openapi.Response(
            description="Başarılı işlem",
            schema=ParcaSerializer
        ),
            400: openapi.Response(
            description="Hata: Yetersiz stok",
            schema=ParcaSerializer
        ),
            404: openapi.Response(
            description="Hata: Parça bulunamadı veya kullanıcıya ait değil.",
            schema=ParcaSerializer
        ),
            403: openapi.Response(
            description="Hata: Kullanıcı takıma ait değil.",
            schema=ParcaSerializer
        ),
    }

)
    def delete(self, request, *args, **kwargs):
        user = request.user

        # Kullanıcı doğrulaması
        if not hasattr(user, 'personel') or not user.personel.takim:
            raise PermissionDenied("Kullanıcının bir takımı yok.")

    
        parca_id = kwargs.get('pk')
        azaltma_miktari = request.query_params.get('stok', 1)  # Varsayılan 1
        try:
            azaltma_miktari = int(azaltma_miktari)  # Integer dönüştür
        except ValueError:
            return Response(
                {"detail": "Stok miktarı geçerli bir sayı olmalıdır."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Parça doğrulama
        try:
            parca = Parca.objects.get(id=parca_id, takim=user.personel.takim)
        except Parca.DoesNotExist:
            return Response(
                {"detail": "Bu parça sizin takımınıza ait değil veya mevcut değil."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Stok miktarını azalt
        if parca.stok > azaltma_miktari:
            parca.stok -= azaltma_miktari
            parca.save()
            return Response(
                {"detail": f"{parca.isim} parçasının stok miktarı {azaltma_miktari} kadar azaltıldı."},
                status=status.HTTP_200_OK
            )
        elif parca.stok == azaltma_miktari:
            parca.delete()
            return Response(
                {"detail": f"{parca.isim} parçası tamamen silindi."},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail": f"Stokta yeterli miktarda {parca.isim} yok."},
                status=status.HTTP_400_BAD_REQUEST
            )