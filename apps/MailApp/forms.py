from django import forms
from django.utils import timezone
from LoginApp.models import KvantUser
from .models import KvantMessage, MailReceiver
from SystemModule.forms import FileStorageSaveForm


class SendNewMails(forms.Form):
    page = forms.IntegerField()

    def save(self, user):
        response = []  # Массив писем
        mail_count = self.cleaned_data['page'] * 8  # Получаем индекс первого письма

        #  Перебор до конца писем или до получения 8
        while len(response) != 8 and mail_count < len(KvantMessage.objects.filter(receivers__receiver=user)):
            mail = KvantMessage.objects.filter(receivers__receiver=user)[mail_count]

            sender = {
                'image': mail.sender.image.image.url,
                'name': ' '.join(mail.sender.__str__().split(' ')[1::]),
            }  # Создание объекта пользователя
            files = [{
                'url': file.file.url,
                'name': file.file.name.split('/')[-1],
            } for file in mail.files.all()]  # Создание объектов файлов
            mail_date = '.'.join(mail.date.__str__().split('-')[::-1])  # Дата отправки
            receiver = mail.receivers.all().filter(receiver=user)[0]  # Текущий получатель

            new_mail = {
                'title': mail.title, 'files': files,
                'date': mail_date, 'text': mail.text,
                'style_text': mail.style_text, 'id': mail.id,
                'sender': sender, 'is_read': receiver.is_read,
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
        date = timezone.now().date()

        mail = KvantMessage.objects.create(
            sender=request.user, style_text=self.cleaned_data['style_text'],
            title=self.cleaned_data['title'], text=self.cleaned_data['text'],
        )
        mail.save()

        for file in request.FILES.getlist('files'):
            file_form = FileStorageSaveForm(
                {'upload_path': f'mail/files/{date}/{mail.title}'}, {'file': file}
            )
            if file_form.is_valid():
                mail.files.add(file_form.save())

        for user_id in request.POST.getlist('receiver'):
            user_form = MailReceiverSaveForm(
                {'receiver': KvantUser.objects.filter(id=int(user_id))[0]}
            )
            if user_form.is_valid():
                mail.receivers.add(user_form.save())
