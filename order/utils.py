# utils.py
from django.db import transaction

@transaction.atomic
def calcular_total_do_pedido(order):
    # Lógica para calcular o total do pedido com base nos itens do pedido
    total = 0
    for item in order.orderitem_set.all():
        total += item.price
    return total