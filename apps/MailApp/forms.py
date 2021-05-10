from django import forms
from .models import KvantMessage


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

            new_mail = {
                'date': mail.date, 'text': mail.text,
                'title': mail.title, 'files': files, 'id': mail.id,
                'sender': sender, 'is_read': mail.is_read
            }  # Формирование представлении письма
            mail_count += 1
            response.append(new_mail)
        return response
