from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import CustomProduct, CustomProductForm, ProductListForm

def home(request):
    products = CustomProduct.objects.all()
    return render(request, 'product/pages/home.html', {'products': products})


@login_required(login_url="user:login_view")
def product_registration(request):
    register_form_data = request.session.get('register_form_data', None)
    form = CustomProductForm(register_form_data)
    return render(request, 'product/pages/product-registration-form.html',{
        'form': form,
        'form_action': reverse('product:product_create'),
    })


@login_required(login_url="user:login_view")
def product_create(request):
    if not request.POST:
        return HttpResponse(status=400)

    POST = request.POST
    request.session['register_form_data'] = POST
    form = CustomProductForm(POST)

    if form.is_valid():
        form.save()
        messages.success(request, 'Produto criado com sucesso.')
        del(request.session['register_form_data'])
        
    return redirect('product:product_registration')


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required(login_url="user:login_view")
def product_list(request):
    form = ProductListForm(request.GET)
    query = form['q'].value()
    if query:
        products = CustomProduct.search_by_productname(query)
    else:
        products = CustomProduct.get_all_products()

    if is_ajax(request):
        data = serialize('json', products)
        return JsonResponse(data, safe=False)

    return render(request, 'product/pages/product-list.html', {'products': products, 'query': query, 'form': form})


@login_required(login_url="user:login_view")
def product_update(request, pk):
    product = get_object_or_404(CustomProduct, pk=pk)

    if request.method == 'POST':
        form = CustomProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso.')
            return redirect('product:product_list')
    else:
        form = CustomProductForm(instance=product)

    return render(request, 'product/pages/product-update-form.html', {'form': form, 'instance': product})



@login_required(login_url="user:login_view")
def delete_product(request, pk):
    product = get_object_or_404(CustomProduct, pk=pk)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Produto excluído com sucesso.')

        # Redirecionar para a lista de produtos após a exclusão
        return redirect('product:product_list')

    # Se a requisição não for POST, redirecionar para a lista de produtos
    return redirect('product:product_list')

@login_required(login_url="user:login_view")
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(CustomProduct, pk=product_id)

        cart = request.session.get('cart', {})
        cart[product_id] = {
            'name': product.name,
            'price': str(product.price),
            'quantity': cart.get(product_id, {}).get('quantity', 0) + 1,
        }

        request.session['cart'] = cart

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})


def search_by_type(request, type):
    products = CustomProduct.search_by_producttype(type)

    if is_ajax(request):
        data = serialize('json', products)
        return JsonResponse(data, safe=False)

    return render(request, 'product/pages/home.html', {'products': products, 'product_type': type})
