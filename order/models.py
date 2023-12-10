from django.db import models
from drop_app import settings
from product.models import CustomProduct

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_completed = models.BooleanField(default=False)
    shipping_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Pedido {self.pk}'
    
    def update_total_amount(self):
        # Atualizar o total_amount do pedido com base nos OrderItems associados
        self.total_amount = sum(item.subtotal for item in self.orderitem_set.all())
        self.save()
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(CustomProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.price
        super().save(*args, **kwargs)

        self.order.update_total_amount()
        self.order.save()

    def __str__(self):
        return f'Pedido {self.pk}'