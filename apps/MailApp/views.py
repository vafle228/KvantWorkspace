from django.http import JsonResponse
from LoginApp.models import KvantUser
from SystemModule.views import is_available
from .models import KvantMessage, ImportantMail
from .forms import SendNewMails, KvantMailSaveForm
from django.shortcuts import render, redirect, HttpResponse


def mail_page(request, identifier):
    # Метод для отображения ящика писем.
    if not is_available(request, identifier):  # Проверка на доступ
        return redirect('/login/')

    sent_mails = len(KvantMessage.objects.filter(sender=request.user))
    important_mails = len(ImportantMail.objects.filter(user=request.user))
    received_mails = len(KvantMessage.objects.filter(receivers__receiver=request.user))

    return render(request, 'MailApp/index.html', {'sent_mails': sent_mails,
                                                  'received_mails': received_mails,
                                                  'users': KvantUser.objects.all(),
                                                  'box_type': request.GET['type'],
                                                  'important_mails': important_mails})


def send_more_mails(request, identifier):
    # Предназначен для условной пагинации ящика
    if not is_available(request, identifier):  # Проверка на доступ
        return redirect('/login/')

    if request.method == 'POST':  # Проверка на POST запрос
        form = SendNewMails(request.POST)  # Формирование формы ответа
        response = form.save(request) if form.is_valid() else []  # Попытка получения данных
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


def change_read_status(request, identifier):
    if not is_available(request, identifier):  # Проверка на доступ
        return redirect('/login/')

    if request.method == 'POST':
        mail_id = request.POST['mail_id']  # id письма из запроса

        if not KvantMessage.objects.filter(id=mail_id).exists():
            return HttpResponse('Error')

        mail = KvantMessage.objects.get(id=mail_id)  # Получаем письмо по id

        # Проверка пользователя на получателя
        if mail.receivers.all().filter(receiver=request.user).exists():
            receiver = mail.receivers.all().filter(receiver=request.user)[0]  # Получатель
            receiver.is_read = True  # Меняем статус
            receiver.save()  # Перезаписываем
            return HttpResponse('Ok')
    return HttpResponse('Error')


def change_important_status(request, identifier):
    if not is_available(request, identifier):
        return redirect('/login/')

    if request.method == 'POST':
        mail_id = request.POST['mail_id']

        if not KvantMessage.objects.filter(id=mail_id).exists():
            return HttpResponse('Error')

        mail = KvantMessage.objects.get(id=mail_id)
        important_mail, created = ImportantMail.objects.get_or_create(user=request.user, mail=mail)
        if not created:
            important_mail.delete()
        return HttpResponse('Ok')
    return HttpResponse('Error')
