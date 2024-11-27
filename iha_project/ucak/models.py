from django.db import models

class Ucak(models.Model):
    isim = models.CharField(max_length=100)
    montaj_sayisi = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.isim