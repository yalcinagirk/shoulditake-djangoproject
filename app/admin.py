from django.contrib import admin
from app import models
# Register your models here.


admin.site.register(models.Product)
admin.site.register(models.Category)
admin.site.register(models.Subcategory)
admin.site.register(models.ProductTitle)

class PageManager(models.Category):

    def get_queryset(self):
        return super(PageManager, self).get_queryset().filter()

