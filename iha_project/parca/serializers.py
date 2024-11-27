from rest_framework import serializers
from .models import Parca

class ParcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parca
        fields = '__all__'

    def validate(self, data):

        request = self.context.get('request')
        user = request.user

        if not hasattr(user, 'personel') or not user.personel.takim:
            raise serializers.ValidationError("Kullanıcının bir takımı yok.")

        kullanici_takimi = user.personel.takim

        # if data.get('takim') and data['takim'] != kullanici_takimi:
        #     raise serializers.ValidationError("Yalnızca kendi takımınıza ait parça üretebilirsiniz.")
        if not kullanici_takimi.parca_turleri.filter(isim=data['isim']).exists():
            raise serializers.ValidationError(
                f"{kullanici_takimi.isim} takımı '{data['isim']}' parçasını üretemez."
            )

        return data
    
    def create(self, validated_data):
        isim = validated_data.get('isim')
        ucak = validated_data.get('ucak')
        takim = validated_data.get('takim')
        stok = validated_data.get('stok', 1)  

        
        parca, created = Parca.objects.get_or_create(
            isim=isim, ucak=ucak, takim=takim,
            defaults={'stok': stok}
        )
        if not created:
            parca.stok += stok
            parca.save()

        return parca

