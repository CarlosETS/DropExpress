from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms.login_form import LoginForm
from .models import CustomUser

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
    return render(request, 'user/pages/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request,'logout success')
    return redirect('user:login_view')