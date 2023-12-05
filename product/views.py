from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import CustomUserForm, LoginForm, EmployeeListForm, EditUserForm
from .models import CustomUser


@login_required(login_url="/login/")
def employee_registration(request):
    register_form_data = request.session.get('register_form_data', None)
    form = CustomUserForm(register_form_data)
    return render(request, 'employee/pages/employee-registration-form.html',{
        'form': form,
        'form_action': reverse('user:employee_create'),
    })


@login_required(login_url="/login/")
def employee_create(request):
    if not request.POST:
        return HttpResponse(status=400)

    POST = request.POST
    request.session['register_form_data'] = POST
    form = CustomUserForm(POST)

    if form.is_valid():
        form.save()
        messages.success(request, 'Funcionario criado com sucesso.')
        del(request.session['register_form_data'])
        
    return redirect('user:employee_registration')


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required(login_url="/login/")
def employee_list(request):
    form = EmployeeListForm(request.GET)
    query = form['q'].value()
    if query:
        employees = CustomUser.search_by_username(query)
    else:
        employees = CustomUser.get_all_employees()

    if is_ajax(request):
        data = serialize('json', employees)
        return JsonResponse(data, safe=False)

    return render(request, 'employee/pages/employee-list.html', {'employees': employees, 'query': query, 'form': form})


@login_required
def employee_update(request, pk):
    instance = get_object_or_404(CustomUser, pk=pk)
    messages.info(request, {instance})
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('user:employee_list')
    else:
        form = EditUserForm(instance=instance)

    return render(request, 'employee/pages/employee-update-form.html', 
        {'form': form, 'instance': instance
    })


@login_required
def delete_user(request, code):
    user = get_object_or_404(CustomUser, code=code)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuário excluído com sucesso.')
    return redirect('user:employee_list')


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
                return redirect('/employee-list/')
            else:
                messages.error(request, "Credenciais inválidas. Tente novamente")
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request,'logout success')
    return redirect('user:login_view')
