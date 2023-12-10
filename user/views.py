from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms.login_form import LoginForm
from .forms.register_form import CustomUserForm
from cart.models import Cart, CartItem
from product.models import CustomProduct

def login_view(request):
    if request.user.is_authenticated:
        return redirect('user:employee_list')

    if request.method=="POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request,"Login Success")
                return redirect('product:home')
            else:
                messages.error(request, "Credenciais inválidas. Tente novamente")
    else:
        form = LoginForm()
    return render(request, 'user/pages/login.html', {'form': form})

@login_required(login_url="user:login_view")
def logout_view(request):
    logout(request)
    messages.success(request,'logout success')
    return redirect('user:login_view')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user:login')
    else:
        form = CustomUserForm()

    return render(request, 'user/pages/register.html', {'form': form})


@login_required(login_url="user:login_view")
def add_to_cart(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = CustomProduct.objects.get(pk=product_id)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()

    return redirect('product:product_list')


@login_required(login_url="user:login_view")
def view_cart(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart/view_cart.html', {'cart_items': cart_items})


@login_required(login_url="user:login_view")
def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(pk=cart_item_id)
    cart_item.delete()
    return redirect('cart:view_cart')
