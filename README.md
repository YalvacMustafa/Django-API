# Django API Projesi

Bu proje, bir **Hava Aracı Üretim Uygulaması** için geliştirilen bir Django API'sidir. Proje, uçak üretim süreçlerini yönetmek ve takip etmek için tasarlanmıştır. API, **takımlar, parçalar, uçaklar** gibi temel özellikleri kapsar.

## Özellikler

- **Takımlar ve Parçalar**:
  - Takımlar: Kanat, Gövde, Kuyruk, Aviyonik, Montaj Takımları.
  - Parçalar: Takımlara özeldir ve yalnızca sorumlu takımlar tarafından üretilebilir.
  - Parçalar üretilebilir, listelenebilir veya geri dönüşüme gönderilebilir.

- **Uçak Üretimi**:
  - Uçak Modelleri: TB2, TB3, AKINCI, KIZILELMA.
  - Montaj Takımı, tüm uygun parçaları birleştirerek uçak üretir.

- **Parca Yönetimi**:
  - Eksik parçalar için envanter uyarıları.
  - Kullanılan parçaların stoktan düşülmesi.

## Proje Gereksinimleri

- **Python**: 3.9.9 veya üstü
- **Django**: 4.2
- **Django Rest Framework**: 3.x
- **PostgreSQL**: 13 veya üstü

## KURULUM

Aşağıdaki adımları izleyerek projeyi kurabilirsiniz:

1. **Proje Deposu**:
   ```bash
   git clone https://github.com/YalvacMustafa/Django-API.git
   cd iha_project
   
2. **Veritabanı Ayarı**:
    Veritabanı tekrardan ayarlanıp settings.py içerisinde güncelleyiniz.
    ```bash
    python manage.py makemigrations
    python manage.py migrate

3. **Verileri İçeri Aktarma**
    - Klasörde yer alan verileri içeri aktarın (json olanlar.)
    - Verileri aktarmak için 
    ```bash
    python manage.py loaddata xxx.json

4. **Uygulamayı Başlatma**
    py manage.py runserver 

## API ENDPOİNTLER VE SWAGGER 

Dokümantasyon
Proje API dokümantasyonuna erişmek için, sunucu çalışıyorken şu adresi ziyaret edin: http://127.0.0.1:8000/swagger/

login işlemi için:
```bash
 http://127.0.0.1:8000/api-auth/login
```
logout işlemi için:

```bash
http://127.0.0.1:8000/api-auth/logout
```
