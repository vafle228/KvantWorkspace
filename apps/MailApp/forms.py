from django import forms
from django.utils import timezone
from LoginApp.models import KvantUser
from SystemModule.forms import FileStorageSaveForm
from .models import KvantMessage, MailReceiver, ImportantMail


class SendNewMails(forms.Form):
    page = forms.IntegerField()

    def save(self, request):
        response = []  # Массив писем
        mail_container = []
        mail_count = self.cleaned_data['page'] * 8  # Получаем индекс первого письма

        if request.GET['type'] == 'received':
            mail_container = [mail for mail in KvantMessage.objects.filter(receivers__receiver=request.user)]

        elif request.GET['type'] == 'sent':
            mail_container = [mail for mail in KvantMessage.objects.filter(sender=request.user)]

        elif request.GET['type'] == 'important':
            mail_container = [mail.mail for mail in ImportantMail.objects.filter(user=request.user)]

        #  Перебор до конца писем или до получения 8
        while len(response) != 8 and mail_count < len(mail_container):
            mail = mail_container[mail_count]

            sender = {
                'image': mail.sender.image.url,
                'permission': mail.sender.permission,
                'name': mail.sender.name,
                'surname': mail.sender.surname,
                'patronymic': mail.sender.patronymic
            }  # Создание объекта пользователя
            files = [{
                'url': file.file.url,
                'name': file.file.name.split('/')[-1],
            } for file in mail.files.all()]  # Создание объектов файлов
            mail_date = '.'.join(mail.date.__str__().split('-')[::-1])  # Дата отправки

            is_read = True
            if request.user != mail.sender:
                is_read = mail.receivers.all().filter(receiver=request.user)[0].is_read  # Текущий получатель

            new_mail = {
                'title': mail.title, 'files': files,
                'date': mail_date, 'text': mail.text,
                'style_text': mail.style_text, 'id': mail.id,
                'sender': sender, 'is_read': is_read,
            }  # Формирование представлении письма
            mail_count += 1
            response.append(new_mail)
        return response


class MailReceiverSaveForm(forms.ModelForm):
    class Meta:
        model = MailReceiver
        fields = ('receiver', )


class KvantMailSaveForm(forms.Form):
    text = forms.CharField()
    style_text = forms.CharField()
    title = forms.CharField(max_length=100)

    def save(self, request):
        date = timezone.now().date()  # Получаем дату письма

        mail = KvantMessage.objects.create(
            sender=request.user, style_text=self.cleaned_data['style_text'],
            title=self.cleaned_data['title'], text=self.cleaned_data['text'],
        )  # Создаем объект письма
        mail.save()  # Сохраняем объект письма

        for file in request.FILES.getlist('files'):  # Перебираем файлы запроса
            file_form = FileStorageSaveForm(
                {'upload_path': f'mail/files/{date}/{mail.title}'}, {'file': file}
            )  # Создаем объект файла
            if file_form.is_valid():  # Проверка валидности файла
                mail.files.add(file_form.save())  # Добавление файла в письмо

        for user_id in request.POST.getlist('receiver'):  # Перебираем получателей
            user_form = MailReceiverSaveForm(
                {'receiver': KvantUser.objects.filter(id=int(user_id))[0]}
            )  # Создаем объект пользователя
            if user_form.is_valid():  # Проверка валидности
                mail.receivers.add(user_form.save())  # Добавление получателей письма
