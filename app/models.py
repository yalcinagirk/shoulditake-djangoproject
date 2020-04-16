from django.db import models
from django.urls import reverse
from unidecode import unidecode
from django.template.defaultfilters import slugify
from uuid import uuid4
import os


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


# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Name:')
    icerik = models.TextField(max_length=2000, blank=True, null=True, verbose_name='Content')
    created_date = models.TimeField(auto_now_add=True, auto_now=False)
    image = models.ImageField(default='/img/default.jpg', upload_to=uplod_to, verbose_name='Image', blank=True)
    categorys = models.ManyToManyField(to=Category, blank=True)
    Subcategorys = models.ManyToManyField(to=Subcategory, blank=True)
    ProductTitles = models.ManyToManyField(to=ProductTitle, blank=True)
    unique_id = models.CharField(max_length=100, editable=True, null=True)
    slug = models.SlugField(null=True, unique=True, editable=False)

    def get_absolute_url(self):
        return reverse('details', kwargs={'slug': self.slug})

    class Meta:
        verbose_name_plural = 'Ürünler'
        ordering = ['id']

    def __str__(self):
        return self.name

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
