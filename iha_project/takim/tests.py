from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Takim

class TakimListCreateViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.takim1 = Takim.objects.create(isim='kanat')
        cls.takim2 = Takim.objects.create(isim='govde')
        cls.url = reverse('takim-list-create')

    def test_get_takim_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['isim'], self.takim1.isim)
        self.assertEqual(response.data[1]['isim'], self.takim2.isim)

    def test_get_takim_list_empty(self):
        Takim.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

