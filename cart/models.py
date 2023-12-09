from django.db import models
from drop_app import settings
from product.models import CustomProduct
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(CustomProduct, through='CartItem')

class CartItem(models.Model):
    product = models.ForeignKey(CustomProduct, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
