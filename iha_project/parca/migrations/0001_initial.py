# Generated by Django 4.2.16 on 2024-11-25 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('takim', '0001_initial'),
        ('ucak', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isim', models.CharField(max_length=100)),
                ('stok', models.PositiveIntegerField(default=0)),
                ('geri_donusumde', models.BooleanField(default=False)),
                ('takim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parcalar', to='takim.takim')),
                ('ucak', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parcalar', to='ucak.ucak')),
            ],
            options={
                'unique_together': {('isim', 'ucak')},
            },
        ),
    ]
