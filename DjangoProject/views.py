from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User, Group
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
            if role == 'customer':
                group, _ = Group.objects.get_or_create(name='пользователь')
            else:
                group, _ = Group.objects.get_or_create(name='аниматор')
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

@login_required
@user_passes_test(is_customer, login_url='index')
def select_offer(request, offer_id):
    offer = AnimatorOffer.objects.get(id=offer_id)
    # Проверяем, есть ли у пользователя незавершённая заявка
    user_request = Request.objects.filter(customer=request.user, status='new').first()
    if user_request:
        user_request.animator = offer.animator  # Привязываем аниматора к заявке
        user_request.status = 'accepted'
        user_request.save()
        messages.success(request, f"Вы выбрали объявление от {offer.animator.username}!")
    else:
        messages.error(request, "У вас нет активных заявок. Сначала создайте заявку.")
    return redirect('offer_list')