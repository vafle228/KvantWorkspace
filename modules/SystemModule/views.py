from django.contrib import messages
from LoginApp.models import KvantUser
from django.shortcuts import render, redirect, HttpResponse


def is_available(request, identifier):
    """
        Метод для проверки доступа на страницу.
        Работет по принципу сравнения запроса и пользователь, что осуществил запрос
    """
    if KvantUser.objects.filter(id=identifier).exists():  # Проверяем существование
        request_user = request.user  # Пользователь который запросил
        requested_user = KvantUser.objects.filter(id=identifier)[0]  # Пользовательн которого запросили
        if request_user == requested_user and requested_user.is_authenticated:  # Проверка совпадения
            return True

    # Ошибка в случаи не совпадения или отсутсвия
    messages.error(request, 'Отказано в доступе!')
    return False


def change_user_theme(request, identifier):
    if not is_available(request, identifier):  # Проверка на доступ
        return redirect('/login/')

    if request.method == 'POST':  # Проверка на POST запрос
        user = KvantUser.objects.filter(id=identifier)[0]  # Получаем пользователя

        user.theme = request.POST['theme']  # Перезаписываем тему
        user.color = request.POST['color']  # Перезаписываем цвет

        user.save()  # Сохраняем изменения
        return HttpResponse('OK')  # Бесполезный ответ
    return HttpResponse('Error')  # Если был не POST запрос или запрет

