from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

    
class Personel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='personel')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    takim = models.ForeignKey('takim.Takim', on_delete=models.SET_NULL, null=True, blank=True, related_name='personeller')

    def save(self, *args, **kwargs):
        
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.user.username} ({self.email})" if self.email else self.user.username
