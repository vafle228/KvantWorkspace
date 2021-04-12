from .models import KvantUser
from django.contrib import messages
from .forms import KvantUserLoginForm
from django.shortcuts import render, redirect


def login_page(request):
    return render(request, 'LoginPage/index.html')


def login_user(request):
    user = None  # Представление пользователя
    if request.method == 'POST':
        form = KvantUserLoginForm(request.POST)  # Форма авторизации
        user = form.save(request) if form.is_valid() else None  # Попытка авторизации
    return redirect('/auth/' if user is None else f'/general/{user.id}/main')


def is_available(request, identifier):
    if KvantUser.objects.filter(id=identifier).exists():  # Проверяем существование
        request_user = request.user  # Пользователь который запросил
        requested_user = KvantUser.objects.filter(id=identifier)[0]  # Пользовательн которого запросили
        if request_user == requested_user and requested_user.is_authenticated:  # Проверка совпадения
            return True

    # Ошибка в случаи не совпадения или отсутсвия
    messages.error(request, 'Отказано в доступе!')
    return False
