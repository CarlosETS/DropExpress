from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize

from product.forms import ProductListForm
from .models import Cart, CartItem
from product.models import CustomProduct
from order.models import Order, OrderItem
from django.utils import timezone

@login_required(login_url="user:login_view")
def add_to_cart(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = CustomProduct.objects.get(pk=product_id)

    # Obtenha a quantidade do formulário
    quantity_from_form = int(request.POST.get('form_quantity', 1))

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if cart_item.quantity == 1:
        cart_item.quantity = quantity_from_form
    else:
        cart_item.quantity += quantity_from_form

    cart_item.save()

    return redirect('cart:view_cart')

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required(login_url="user:login_view")
def view_cart(request):

    products = CustomProduct.objects.all()
    form = ProductListForm(request.GET)
    query = form['q'].value()
    if query:
        products = CustomProduct.search_by_productname(query)
    else:
        products = CustomProduct.get_all_products()

    if is_ajax(request):
        data = serialize('json', products)
        return JsonResponse(data, safe=False)
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


@login_required(login_url="user:login_view")
def update_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            cart_item.quantity = max(cart_item.quantity - 1, 1)
        cart_item.save()
    return redirect('cart:view_cart')

@login_required(login_url="user:login_view")
def convert_cart_to_order(request):
    order = None  # Define the variable outside the try block

    try:
        cart = Cart.objects.get(user=request.user)
        order, created = Order.objects.get_or_create(
            user=request.user,
            defaults={
                'created_at': timezone.now(),
                'total_amount': 0,
                'is_completed': False,
                'shipping_address': '',
            }
        )
    except Cart.DoesNotExist:
        # Se não existir, cria um novo
        cart = Cart.objects.create(user=request.user)
    
    cart_items = CartItem.objects.filter(cart=cart)

    total_price = 0
    for cart_item in cart_items:
        order_item = OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.price,
        )
        total_price += order_item.subtotal

    if order:
        order.total_amount = total_price
        order.save()

    # Limpa o carrinho
    cart_items.delete()

    return redirect('order:order_list')