from LoginApp.models import KvantUser
from django.contrib import messages
from django.shortcuts import render


def test(request):
    return render(request, 'SystemModule/AsideMenu/index.html')


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

