from rest_framework import serializers
from .models import Takim


class TakimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Takim
        fields = '__all__'
