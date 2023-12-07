from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import CustomProduct, CustomProductForm

@login_required(login_url="/login/")
def product_registration(request):
    register_form_data = request.session.get('register_form_data', None)
    form = CustomProductForm(register_form_data)
    return render(request, 'product/pages/product-registration-form.html',{
        'form': form,
        'form_action': reverse('product:product_create'),
    })


@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
def product_list(request):
    form = CustomProductForm(request.GET)
    query = form['q'].value()
    if query:
        products = CustomProduct.search_by_username(query)
    else:
        products = CustomProduct.get_all_products()

    if is_ajax(request):
        data = serialize('json', products)
        return JsonResponse(data, safe=False)

    return render(request, 'product/pages/product-list.html', {'products': products, 'query': query, 'form': form})


@login_required(login_url="/login/")
def product_update(request, pk):
    instance = get_object_or_404(request, pk=pk)  # Substitua 'Product' pelo seu modelo real
    if request.method == 'POST':
        form = CustomProductForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')  # Mensagem de sucesso
            return redirect('product:product_list')
        else:
            messages.error(request, 'Error updating product. Please check the form.')  # Mensagem de erro
    else:
        form = CustomProductForm(instance=instance)

    return render(request, 'product/pages/product-update-form.html', 
                  {'form': form, 'instance': instance})


@login_required(login_url="/login/")
def delete_product(request, pk):
    product = get_object_or_404(CustomProduct, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Usuário excluído com sucesso.')
    return redirect('product:product_list')