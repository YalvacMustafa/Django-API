from django.db import models

class Takim(models.Model):
    isim = models.CharField(max_length=100)

    def __str__(self):
        return self.isim

class ParcaTuru(models.Model):
    isim = models.CharField(max_length=100, unique=True)  
    takim = models.ForeignKey(Takim, on_delete=models.CASCADE, related_name='parca_turleri')

    def __str__(self):
        return f"{self.isim} ({self.takim.isim})"