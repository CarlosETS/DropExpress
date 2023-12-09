from django.db import models
from product.models import CustomProduct
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_completed = models.BooleanField(default=False)
    shipping_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Pedido {self.pk}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(CustomProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Outros campos relacionados ao item do pedido podem ser adicionados conforme necessário

    def __str__(self):
        return f'Item do Pedido {self.pk}'