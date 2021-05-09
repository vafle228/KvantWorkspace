from .forms import SendNewMails
from .models import KvantMessage
from django.http import JsonResponse
from LoginApp.models import KvantUser
from SystemModule.views import is_available
from django.shortcuts import render, redirect, HttpResponse


def mail_page(request, identifier):
    """
        Метод для отображения ящика писем.
        Механиз отправки писем реализован через AJAX на стороне FrontEnd
    """
    if not is_available(request, identifier):  # Проверка на доступ
        return redirect('/login/')

    receiver = KvantUser.objects.filter(id=identifier)[0]
    is_mail = bool(len(KvantMessage.objects.filter(receiver=receiver)))
    return render(request, 'MailApp/index.html', {'is_mail': is_mail})


def send_more_mails(request, identifier):
    """
        Метод для AJAX запроса с FrontEnd.
        Предназначен для условной пагинации ящика с письмами
    """
    if not is_available(request, identifier):  # Проверка на доступ
        return redirect('/login/')

    if request.method == 'POST':  # Проверка на POST запрос
        form = SendNewMails(request.POST)  # Формирование формы ответа
        user = KvantUser.objects.filter(id=identifier)[0]  # Пользователь запрос
        response = form.save(user) if form.is_valid() else []  # Попытка получения данных
        return JsonResponse({'mails': response})  # JSON ответ
    return HttpResponse('Error')  # В случаи ошибки ранее


def change_mail_status(request, identifier):
    if not is_available(request, identifier):
        return redirect('/login/')

    if request.method == 'POST':
        mail_id = request.POST['mail_id']
        mail = KvantMessage.objects.filter(id=mail_id)[0]

        mail.is_read = True
        mail.save()
        return HttpResponse('OK')
    return HttpResponse('Error')
