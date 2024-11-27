from django.db import models

class Parca(models.Model):
    isim = models.CharField(max_length=100)
    takim = models.ForeignKey('takim.Takim', on_delete=models.CASCADE, related_name='parcalar')
    ucak = models.ForeignKey('ucak.Ucak', on_delete=models.CASCADE, related_name='parcalar', null=True, blank=True)
    stok = models.PositiveIntegerField(default=0)


    def __str__(self):
        return f'{self.isim} ({self.stok}) - {self.ucak}'