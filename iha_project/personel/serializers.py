from rest_framework import serializers
from .models import Personel


class PersonelSerializer(serializers.ModelSerializer):
    takim = serializers.StringRelatedField(read_only=True) #Takım adını göstermek için
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}) #Şifre sadece yazılabilir
    class Meta:
        model = Personel
        fields = '__all__'

    def validate(self, data):
        if 'takim' in self.initial_data:
            raise serializers.ValidationError({
                'non_field_errors': ['Kayıt sırasında takım bilgisi gönderilemez.']
            })
        return data