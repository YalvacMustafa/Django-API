from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from personel.models import Personel
from django.urls import reverse

class PersonelDetailViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword") # Kullanıcı ve Personel oluştur
        self.personel = Personel.objects.create(
            user=self.user,
            email="test@example.com",
            password="testpassword"  # Şifre make_password ile hashlenir
        )

        self.url = reverse('personel-detail', kwargs={'pk': self.personel.pk}) # Test için kullanılan URL

    def test_get_personel_detail_authenticated(self):
        """
        Giriş yapmış kullanıcı kendi Personel profilini alabilmeli.
        """

        self.client.login(username="testuser", password="testpassword") # Kullanıcıyı oturum açmış şekilde ayarla
        response = self.client.get(self.url)# GET isteği gönder
        
        self.assertEqual(response.status_code, status.HTTP_200_OK) # Yanıtı kontrol et
        self.assertEqual(response.data['email'], self.personel.email)
        self.assertIn('takim', response.data)  # Takım bilgisi döndü mü?

    def test_get_personel_detail_unauthenticated(self):
        """
        Giriş yapmamış kullanıcı erişim sağlamamalı.
        """

        response = self.client.get(self.url)# Giriş yapmadan GET isteği gönder
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)# Yanıtı kontrol et

    def test_get_personel_detail_no_profile(self):
        """
        Giriş yapmış kullanıcı için Personel profili yoksa 403 döner.
        """
        new_user = User.objects.create_user(username="newuser", password="newpassword")  # Başka bir kullanıcı oluştur, ancak ona Personel atanmasın
        self.client.login(username="newuser", password="newpassword")
        response = self.client.get(reverse('personel-detail', kwargs={'pk': 999})) # GET isteği gönder # Var olmayan bir PK
       
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) # Yanıtı kontrol et
        self.assertIn("Profiliniz bulunamadı.", str(response.data))


