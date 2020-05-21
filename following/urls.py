from django.conf.urls import include, url
from following.views import kullanici_takip_et_cikar

urlpatterns = [
    url(r'^takiplesme-sistemi/$', kullanici_takip_et_cikar, name='kullanici_takip_et_cikar'),
]
