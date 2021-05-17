from .models import KvantMessage
from django.http import JsonResponse
from LoginApp.models import KvantUser
from SystemModule.views import is_available
from .forms import SendNewMails, KvantMailSaveForm
from django.shortcuts import render, redirect, HttpResponse


def mail_page(request, identifier):
    # Метод для отображения ящика писем.
    if not is_available(request, identifier):  # Проверка на доступ
        return redirect('/login/')
    max_mails = len(KvantMessage.objects.filter(receivers__receiver=request.user))
    return render(request, 'MailApp/index.html', {'max_mails': max_mails, 'users': KvantUser.objects.all()})


def send_more_mails(request, identifier):
    # Предназначен для условной пагинации ящика
    if not is_available(request, identifier):  # Проверка на доступ
        return redirect('/login/')

    if request.method == 'POST':  # Проверка на POST запрос
        form = SendNewMails(request.POST)  # Формирование формы ответа
        user = KvantUser.objects.filter(id=identifier)[0]  # Пользователь запроса
        response = form.save(user) if form.is_valid() else []  # Попытка получения данных
        return JsonResponse({'mails': response})  # JSON ответ
    return HttpResponse('Error')  # В случаи ошибки ранее


def create_mail(request, identifier):
    if not is_available(request, identifier):  # Проверка на доступ
        return redirect('/login/')

    if request.method == 'POST':
        form = KvantMailSaveForm(request.POST)  # Форма создания письма
        form.save(request) if form.is_valid() else None  # Попытка создать письмо
        return HttpResponse('Ok')  # Ответ для прикола
    return HttpResponse('Error')  # Если была ошибка ранее


def change_mail_status(request, identifier):
    if not is_available(request, identifier):  # Проверка на доступ
        return redirect('/login/')

    if request.method == 'POST':
        mail_id = request.POST['mail_id']  # id письма из запроса
        mail = KvantMessage.objects.filter(id=mail_id)[0]  # Получаем письмо по id

        if mail.receivers.all().filter(receiver=request.user).exists():  # Проверка пользователя на получателя
            receiver = mail.receivers.all().filter(receiver=request.user)[0]  # Получатель

            receiver.is_read = True  # Меняем статус
            receiver.save()  # Перезаписываем
            return HttpResponse('OK')
    return HttpResponse('Error')
