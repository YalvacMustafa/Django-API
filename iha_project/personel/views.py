from .models import Personel
from .serializers import PersonelSerializer
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from drf_yasg import openapi

class PersonelDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Personel Hesabı',
        operation_description='Giriş yapmış kullanıcıya ait personel profilini getirir.',
        responses={
            200: openapi.Response(
                description='Başarılı Yanıt',
                schema=PersonelSerializer(),
            ),
            403: openapi.Response(description='İzin Reddedildi', schema=PersonelSerializer),
            404: openapi.Response(description='Profiliniz bulunamadı', schema=PersonelSerializer),
        },
    )
    def get(self, request, *args, **kwargs):
        try:
            personel = Personel.objects.get(user=request.user)  
        except Personel.DoesNotExist:
            raise PermissionDenied('Profiliniz bulunamadı.')  

        serializer = PersonelSerializer(personel)
        return Response(serializer.data, status=status.HTTP_200_OK)