from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.db.models.signals import post_save
# Create your models here.
class UserProfile(models.Model):
    Cinsiyet = ((None, 'Cinsiyet'), ('diger', 'DİĞER'), ('erkek', 'ERKEK'), ('kadın', 'KADIN'))

    user = models.OneToOneField(User, null=True, blank=False, verbose_name='User', on_delete=models.CASCADE)
    bio = models.TextField(max_length=1000, verbose_name='Hakkımda', blank=True, null=True)
    profile_photo = models.ImageField(null=True, blank=True, verbose_name='Profil Fotoğrafı')
    dogum_tarihi = models.DateField(null=True, blank=True, verbose_name='Doğum Tarihi')
    cinsiyet = models.CharField(choices=Cinsiyet, blank=True, max_length=6, verbose_name='Cinsiyet')

    class Meta:
        verbose_name_plural = "Kullanici Profilleri"

    def get_screen_name(self):
        user = self.user
        if user.get_full_name():
            return user.get_full_name()
        return user.username

    def __str__(self):
        return "%s Profile" % self.get_screen_name()

    def get_user_profile_url(self):
        url = reverse('user_profile', kwargs={'username': self.user.username})
        return url

    def get_profile_photo(self):
        if self.profile_photo:
            print(self.profile_photo.url + "**************")
            return self.profile_photo.url
        return "/static/img/default_image.jpg"

def create_profile(sender, created, instance,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)
post_save.connect(create_profile, sender=User)