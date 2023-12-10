from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from .forms import CreditCardForm

@login_required(login_url="user:login_view")
def process_order(request, pk):

    order = get_object_or_404(Order, user=request.user, is_completed=False, pk=pk)

    if request.method == 'POST':
        return redirect('order:process_order', pk=order.id)

    context = {
        'order': order,
    }

    return render(request, 'orders/pages/process-order.html', context)

@login_required(login_url="user:login_view")
def order_confirmation(request, pk):
    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        return render(request, 'orders/pages/order-not-found.html')

    if request.method == 'POST':
        credit_card_form = CreditCardForm(request.POST)
        if credit_card_form.is_valid():
            # Lógica para processar os dados do cartão de crédito
            # ...S

            # Marque o pedido como concluído
            order.is_completed = True
            order.save()

            return redirect('order:order_confirmation', pk=order.id)

    else:
        credit_card_form = CreditCardForm()

    context = {
        'order': order,
        'total_amount': order.total_amount,
        'credit_card_form': credit_card_form,
    }

    return render(request, 'orders/pages/order-confirmation.html', context)

@login_required(login_url="user:login_view")
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/pages/order-list.html', {'orders': orders})


@login_required(login_url="user:login_view")
def order_detail(request, pk):
    # Tenta obter o pedido do usuário
    order = get_object_or_404(Order, id=pk, user=request.user)

    # Obtém os itens do pedido
    order_items = OrderItem.objects.filter(order=order)

    # Calcular subtotal e total_price
    total_price = 0
    for order_item in order_items:
        order_item.subtotal = order_item.quantity * order_item.product.price
        total_price += order_item.subtotal
        order_item.save()  # Salvar a alteração no subtotal

    return render(request, 'orders/pages/order-detail.html', {'order': order, 'order_items': order_items, 'total_price': total_price})