from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Ucak

class UcakListCreateViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.ucak1 = Ucak.objects.create(isim='TBA2')
        cls.ucak2 = Ucak.objects.create(isim='AKINCI')
        cls.url = reverse('ucak-list')

    def test_get_ucak_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['isim'], self.ucak1.isim)
        self.assertEqual(response.data[1]['isim'], self.ucak2.isim)
    
    def test_get_ucak_list_empty(self):
        Ucak.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
