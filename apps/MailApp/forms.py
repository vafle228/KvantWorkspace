from django import forms
from .models import KvantMessage
from django.utils import timezone
from LoginApp.models import KvantUser
from SystemModule.forms import FileStorageSaveForm


class SendNewMails(forms.Form):
    page = forms.IntegerField()

    def save(self, user):
        response = []  # Массив писем
        mail_count = self.cleaned_data['page'] * 8  # Получаем индекс первого письма

        #  Перебор до конца писем или до получения 8
        while len(response) != 8 and mail_count < len(KvantMessage.objects.filter(receiver=user)):
            mail = KvantMessage.objects.filter(receiver=user)[::-1][mail_count]

            sender = {
                'image': mail.sender.image.image.url,
                'name': ' '.join(mail.sender.__str__().split(' ')[1::]),
            }  # Создание объекта пользователя
            files = [{
                'url': file.file.url,
                'name': file.file.name.split('/')[-1],
            } for file in mail.files.all()]  # Создание объектов файлов
            mail_date = '.'.join(mail.date.__str__().split('-')[::-1])

            new_mail = {
                'date': mail_date, 'text': mail.text,
                'title': mail.title, 'files': files,
                'sender': sender, 'is_read': mail.is_read,
                'style_text': mail.style_text, 'id': mail.id,
            }  # Формирование представлении письма
            mail_count += 1
            response.append(new_mail)
        return response


class KvantMailSaveForm(forms.Form):
    text = forms.CharField()
    style_text = forms.CharField()
    title = forms.CharField(max_length=100)

    def save(self, request):
        sender = request.user
        date = timezone.now().date()
        text = self.cleaned_data['text']
        title = self.cleaned_data['title']
        style_text = self.cleaned_data['style_text']
        receiver = KvantUser.objects.filter(id=request.POST['receiver'])[0]

        mail = KvantMessage.objects.create(
            sender=sender, text=text, title=title,
            receiver=receiver, style_text=style_text
        )
        mail.save()

        for file in request.FILES.getlist('files'):
            file_form = FileStorageSaveForm(
                {'upload_path': f'mail/files/{date}/{title}'}, {'file': file}
            )
            if file_form.is_valid():
                mail.files.add(file_form.save())
