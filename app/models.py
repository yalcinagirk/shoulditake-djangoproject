from django.db import models
from django.urls import reverse
from unidecode import unidecode
from django.template.defaultfilters import slugify
from uuid import uuid4
import os
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db.models.signals import post_save

def uplod_to(instance, filename):
    uzanti = filename.split('.')[-1]
    new_name = '%s.%s' % (str(uuid4()), uzanti)
    unique_id = instance.unique_id
    return os.path.join('product', unique_id, new_name)


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Kategori')

    class Meta:
        verbose_name_plural = 'Kategoriler'

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=50, verbose_name='Alt Kategori')
    topCategory = models.ManyToManyField(to=Category, blank=True)

    class Meta:
        verbose_name_plural = 'Alt Kategoriler'

    def __str__(self):
        return self.name


class ProductTitle(models.Model):
    name = models.CharField(max_length=50, verbose_name='Ürün Başlığı')
    subcategory = models.ManyToManyField(to=Subcategory, blank=True)

    class Meta:
        verbose_name_plural = 'Ürün Başlıkları'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Name:')
    user = models.ForeignKey(User, default=1, null=True, verbose_name='User', related_name='product',
                             on_delete=models.CASCADE)
    icerik = RichTextField(null=True, blank=False, max_length=5000, verbose_name="İçerik giriniz...")
    created_date = models.TimeField(auto_now_add=True, auto_now=False)
    image = models.ImageField(default='/img/default.jpg', upload_to=uplod_to, verbose_name='Image', blank=True)
    categorys = models.ManyToManyField(to=Category, blank=True)
    Subcategorys = models.ManyToManyField(to=Subcategory, blank=True)
    ProductTitles = models.ManyToManyField(to=ProductTitle, blank=True)
    unique_id = models.CharField(max_length=100, editable=True, null=True)
    slug = models.SlugField(null=True, unique=True, editable=False)

    def get_absolute_url(self):
        return reverse('details', kwargs={'slug': self.slug})

    def get_added_favorite_user(self):
        return self.favorite.values_list('user__username', flat=True)


    def get_comment_count(self):
        yorum_sayisi = self.comment.count()
        if yorum_sayisi > 0:
            return yorum_sayisi
        return "Henüz yorum yok."
    def get_favori_count(self):
        fovori_sayisi = self.favorite.count()
        if fovori_sayisi > 0:
            return fovori_sayisi
        return "Henüz favori yok."


    class Meta:
        verbose_name_plural = 'Ürünler'
        ordering = ['-id']

    def __str__(self):
        return "%s (%s)" % (self.name, self.user)

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return '/img/default.jpg'

    def get_unique_sluq(self):
        sayi = 0
        slug = slugify(unidecode(self.name))
        new_slug = slug
        while Product.objects.filter(slug=new_slug).exists():
            sayi += 1
            new_slug = "%s-%s" % (slug, sayi)
        slug = new_slug
        return slug

    def save(self, *args, **kwargs):
        if self.id is None:
            self.unique_id = str(uuid4())
            self.slug = self.get_unique_sluq()

        else:
            product = Product.objects.get(slug=self.slug)
            if product.name != self.name:
                self.slug = self.get_unique_sluq()

        super(Product, self).save(*args, **kwargs)

    def get_product_comment(self):
        # gönderiye ait yorumları aldık
        return self.comment.all()

    def get_blog_comment_count(self):
        # gönderiye ait yorumları aldık
        return len(self.get_product_comment())


class Comment(models.Model):
    user = models.ForeignKey(User, null=True, default=1, related_name='comment', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE, related_name='comment')
    icerik = models.TextField(verbose_name="Yorum", max_length=1000, blank=False, null=True)
    comment_date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = 'Yorumlar'

    def __str__(self):
        return "%s %s" % (self.user, self.product)

    def get_screen_name(self):
        if self.user.first_name:
            return "%s" % (self.user.get_full_name())
        return self.user.username


class FavoritedProduct(models.Model):
    user = models.ForeignKey(User, null=True, default=1, related_name='favorite', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE, related_name='favorite')

    def __str__(self):
        return "%s %s" % (self.user, self.product)



    class Meta:
        verbose_name_plural = 'Favori Ürünler'

def update_product(sender, created, instance,**kwargs):
    if created:
        Product.objects.create(user=instance)
post_save.connect(update_product, sender=User)
