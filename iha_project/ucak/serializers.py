from rest_framework import serializers
from .models import Ucak

class UcakSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ucak
        fields = '__all__'