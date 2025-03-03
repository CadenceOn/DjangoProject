from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test  # Добавляем импорт user_passes_test
from django.contrib import messages
from django.contrib.auth.models import Group
from .forms import RegisterForm, RequestForm, AnimatorOfferForm
from .models import Request, AnimatorOffer

def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Добро пожаловать, {username}!")
                return redirect('index')
            else:
                messages.error(request, "Неверное имя пользователя или пароль.")
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            if role == 'customer':  # Исправляем 'сustomer' на 'customer'
                group, _ = Group.objects.get_or_create(name='customer')  # Исправляем название группы на 'customer'
            else:
                group, _ = Group.objects.get_or_create(name='animator')  # Исправляем на 'animator'
            user.groups.add(group)
            username = form.cleaned_data.get('username')
            messages.success(request, f"Аккаунт для {username} успешно создан! Теперь вы можете войти.")
            return redirect('login')
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect('index')

def is_customer(user):
    return user.groups.filter(name='customer').exists()

@login_required
@user_passes_test(is_customer, login_url='index')
def create_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.customer = request.user
            new_request.save()
            messages.success(request, "Заявка успешно создана!")
            return redirect('index')
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме: " + str(form.errors))
    else:
        form = RequestForm()
    return render(request, 'create_request.html', {'form': form})

def is_animator(user):
    return user.groups.filter(name='animator').exists()

@login_required
@user_passes_test(is_animator, login_url='index')
def create_offer(request):
    if request.method == 'POST':
        form = AnimatorOfferForm(request.POST)
        if form.is_valid():
            new_offer = form.save(commit=False)
            new_offer.animator = request.user
            new_offer.save()
            messages.success(request, "Объявление успешно создано!")
            return redirect('index')
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме: " + str(form.errors))
    else:
        form = AnimatorOfferForm()
    return render(request, 'create_offer.html', {'form': form})

@login_required
@user_passes_test(is_customer, login_url='index')
def offer_list(request):
    offers = AnimatorOffer.objects.all()
    return render(request, 'offer_list.html', {'offers': offers})

