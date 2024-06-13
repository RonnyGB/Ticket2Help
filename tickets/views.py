# views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .ticket_helper import *
from .forms import RegisterForm


def index(request):
    return render(request, 'tickets/index.html')


def list_tickets(request, tipo=0):
    tickets = get_tickets(op=tipo)
    user = request.user
    if user.is_staff or user.has_perm('app_name.permission_codename'):
        return render(request, 'home/technic/list_tickets.html', {'tickets': tickets})
    else:
        return render(request, 'home/client/list_tickets.html', {'tickets': tickets})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            firstname = form.cleaned_data.get('firstname')
            lastname = form.cleaned_data.get('lastname')
            password = form.cleaned_data.get('password1')
            User.objects.create_user(username=username, email=email, password=password, first_name=firstname,
                                     last_name=lastname)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def home(request):
    user = request.user
    if user.is_staff or user.has_perm('app_name.permission_codename'):
        return render(request, 'home/technic.html')
    else:
        return render(request, 'home/client.html')
