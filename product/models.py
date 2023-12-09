from django.db import models
from enum import Enum

class ProductType(Enum):
    MOBILE = 'Mobile'
    TV = 'TV'
    CAMERA = 'Camera'
    LAPTOP = 'Laptop'
    TABLET = 'Tablet'
    SPEAKER = 'Speaker'

class CustomProduct(models.Model):
    name = models.CharField(max_length=255)
    product_type = models.CharField(max_length=20, choices=[(tag.name, tag.value) for tag in ProductType])
    description = models.CharField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField()
    image = models.ImageField(upload_to='product_images/', blank= True, null=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_all_products(cls):
        return cls.objects.all()

    @classmethod
    def search_by_productname(cls, name):
        return cls.objects.filter(name__icontains=name)

    @classmethod
    def search_by_producttype(cls, product_type):
        return cls.objects.filter(product_type__icontains=product_type)


    @classmethod
    def filter_by_available_stock(cls):
        return cls.objects.filter(stock__gt=0)
