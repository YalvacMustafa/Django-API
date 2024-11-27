from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Parca
from takim.models import Takim
from personel.models import Personel
from django.contrib.auth.hashers import make_password
from takim.models import ParcaTuru


class ParcaListCreateViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Kullanıcı ve Takım oluşturma
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.takim = Takim.objects.create(isim='Kanat Takımı')
        cls.personel = Personel.objects.create(
            user=cls.user,
            email='testuser@example.com',
            password=make_password('testpassword'),
            takim=cls.takim,
        )

        # Parça Türleri oluşturma
        cls.parca_turu1 = ParcaTuru.objects.create(isim='Kanat', takim=cls.takim)
        cls.parca_turu2 = ParcaTuru.objects.create(isim='Aviyonik', takim=cls.takim)

        # Başka bir takım ve tür
        cls.other_takim = Takim.objects.create(isim='Gövde Takımı')
        cls.other_parca_turu = ParcaTuru.objects.create(isim='Gövde', takim=cls.other_takim)

        # Parçalar
        cls.parca1 = Parca.objects.create(isim='Kanat', takim=cls.takim, stok=10)
        cls.parca2 = Parca.objects.create(isim='Aviyonik', takim=cls.takim, stok=5)

        # Endpoint URL
        cls.url = reverse('parca-list-create') 

    def setUp(self):
        self.client.login(username='testuser', password='testpassword')

    def test_get_parcalar(self):
        """Kullanıcı yalnızca kendi takımına ait parçaları görebilmeli"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['isim'], self.parca1.isim)
        self.assertEqual(response.data[1]['isim'], self.parca2.isim)

    def test_get_parcalar_no_team(self):
        """Takımı olmayan kullanıcı parça görememeli"""
        self.personel.takim = None
        self.personel.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    