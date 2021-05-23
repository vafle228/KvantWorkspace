from .forms import KvantUserLoginForm
from django.shortcuts import render, redirect


def login_page(request):
    """Отображение страницы авторизации"""
    return render(request, 'LoginApp/index.html')


def login_user(request):
    user = None  # Представление пользователя
    if request.method == 'POST':
        form = KvantUserLoginForm(request.POST)  # Форма авторизации
        user = form.save(request) if form.is_valid() else None  # Попытка авторизации
    return redirect('/login/' if user is None else f'/news/{user.id}/main')
