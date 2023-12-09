from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order
from .forms import CreditCardForm

@login_required(login_url="user:login_view")
def process_order(request):
    # Lógica para processar o pedido...

    if request.method == 'POST':
        credit_card_form = CreditCardForm(request.POST)
        if credit_card_form.is_valid():
            # Lógica para processar os dados do cartão de crédito
            # ...
            
            # Marcar o pedido como concluído
            Order.is_completed = True
            Order.save()

            # Redirecionar para a página de confirmação de pedido
            return redirect('cart:order_confirmation')
    else:
        credit_card_form = CreditCardForm()

    context = {
        'order': Order,
        'credit_card_form': credit_card_form,
    }

    return render(request, 'cart/process_order.html', context)