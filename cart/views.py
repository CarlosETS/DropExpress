from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from product.models import CustomProduct

@login_required(login_url="user:login_view")
def add_to_cart(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = CustomProduct.objects.get(pk=product_id)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    created.save()

    return redirect('product:product_list')

@login_required(login_url="user:login_view")
def view_cart(request):
    # Tenta obter o carrinho do usuário
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        # Se não existir, cria um novo
        cart = Cart.objects.create(user=request.user)

    # Obtém os itens do carrinho
    cart_items = CartItem.objects.filter(cart=cart)
    
    total_price = 0

    for cart_item in cart_items:
        cart_item.subtotal = cart_item.quantity * cart_item.product.price
        total_price += cart_item.subtotal

    return render(request, 'cart/pages/cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required(login_url="user:login_view")
def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(pk=cart_item_id)
    cart_item.delete()
    return redirect('cart:view_cart')
