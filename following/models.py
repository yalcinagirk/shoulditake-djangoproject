from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Following(models.Model):
    follower = models.ForeignKey(User, related_name='follower', null=True, verbose_name="Takip eden kullanıcı",
                                 on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='following', null=True, verbose_name="Takip edilen kullanıcı",
                                 on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Takipleşme Sistemi"

    def __str__(self):
        return "Follower {} - Followed {}".format(self.follower.username, self.followed)

    @classmethod
    def kullanici_takip_et(cls, follower, followed):
        cls.objects.create(follower=follower, followed=followed)

    @classmethod
    def kullaniciyi_takip_ediyor_mu(cls, follower, followed):
        return cls.objects.filter(follower=follower, followed=followed).exists()

    @classmethod
    def kullaniciyi_takipten_cikar(cls, follower, followed):
        cls.objects.filter(follower=follower, followed=followed).delete()

    @classmethod
    def kullaniciyi_takip_edilenler_ve_takipciler(cls, user):
        data = {'takip_edilenler': 0, 'takipciler': 0}
        takip_edilenler = cls.objects.filter(follower=user).count()
        takipciler = cls.objects.filter(followed=user).count()

        data.update({'takip_edilenler': takip_edilenler, 'takipciler': takipciler})
        return data
