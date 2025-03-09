from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from .forms import RegisterForm, RequestForm, AnimatorOfferForm
from .models import Request, AnimatorOffer
import json

# Проверка ролей
def is_customer(user):
    return user.groups.filter(name='customer').exists()

def is_animator(user):
    return user.groups.filter(name='animator').exists()

# Главная страница
def index(request):
    offers = AnimatorOffer.objects.all()
    return render(request, 'index.html', {'offers': offers})

# Регистрация
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            if role == 'customer':
                group, _ = Group.objects.get_or_create(name='customer')
            else:
                group, _ = Group.objects.get_or_create(name='animator')
            user.groups.add(group)
            username = form.cleaned_data.get('username')
            messages.success(request, f"Аккаунт для {username} успешно создан! Теперь вы можете войти.")
            return redirect('login')
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# Вход
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    return render(request, 'login.html')

# Выход
def logout_view(request):
    logout(request)
    return redirect('index')

# Создание заявки (для пользователей)
@login_required
@user_passes_test(is_customer)
def create_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.customer = request.user
            new_request.save()
            messages.success(request, 'Заявка успешно создана!')
            return redirect('index')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = RequestForm()
    return render(request, 'create_request.html', {'form': form})

# Создание объявления (для аниматоров)
@login_required
@user_passes_test(is_animator)
def create_offer(request):
    if request.method == 'POST':
        form = AnimatorOfferForm(request.POST, request.FILES)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.animator = request.user
            offer.save()
            messages.success(request, 'Объявление успешно создано!')
            return redirect('index')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = AnimatorOfferForm()
    return render(request, 'create_offer.html', {'form': form})

# Список объявлений (для пользователей)
def offer_list(request):
    offers = AnimatorOffer.objects.all()
    return render(request, 'offer_list.html', {'offers': offers})

# Выбор объявления (для пользователей)
@login_required
@user_passes_test(is_customer)
def select_offer(request, offer_id):
    offer = get_object_or_404(AnimatorOffer, id=offer_id)
    request_obj = Request.objects.filter(customer=request.user, animator__isnull=True).first()
    if request_obj:
        request_obj.animator = offer.animator
        request_obj.status = 'accepted'
        request_obj.save()
        messages.success(request, 'Аниматор успешно выбран!')
    else:
        messages.error(request, 'У вас нет активных заявок.')
    return redirect('offer_list')

# Просмотр заявок (для аниматоров)
@login_required
@user_passes_test(is_animator)
def view_requests(request):
    requests = Request.objects.filter(animator=request.user, status='accepted')
    return render(request, 'view_requests.html', {'requests': requests})

# Профиль аниматора (редактирование карточки)
@login_required
@user_passes_test(is_animator)
def my_profile(request):
    offer = AnimatorOffer.objects.filter(animator=request.user).first()
    if request.method == 'POST':
        form = AnimatorOfferForm(request.POST, request.FILES, instance=offer)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.animator = request.user
            offer.save()
            messages.success(request, 'Карточка успешно обновлена!')
            return redirect('my_profile')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = AnimatorOfferForm(instance=offer)
    return render(request, 'my_profile.html', {'form': form, 'offer': offer})