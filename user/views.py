from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms.login_form import LoginForm
from .forms.register_form import CustomUserForm

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
                return redirect('product:product_list')
            else:
                messages.error(request, "Credenciais inválidas. Tente novamente")
    else:
        form = LoginForm()
    return render(request, 'user/pages/login.html', {'form': form})

@login_required
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