from django import forms
from .models import KvantNews
from django.utils import timezone
from StudentPage.forms import FileStorageSaveForm, ImageStorageSaveForm


class KvantNewsSaveForm(forms.Form):
    content = forms.CharField()
    title = forms.CharField(max_length=100)

    def save(self, request):
        #  Считываем данные с запроса
        title = self.cleaned_data['title']
        content = self.cleaned_data['content']
        date = timezone.now().date()

        news = KvantNews.objects.create(
            content=content, title=title, author=request.user
        )  # Создание новости

        image_form = ImageStorageSaveForm(
            {'upload_path': f'news/images/{date}/{title}'}, request.FILES
        )  # Создание превью новости
        if image_form.is_valid():  # Проверка валидности фото
            news.image = image_form.save()  # Замена дефолтного превью

        news.save()  # Пресохранение новости

        for file in request.FILES.getlist('files'):  # Добавление файлов в новость
            file_form = FileStorageSaveForm(
                {'upload_path': f'news/files/{date}/{title}'}, {'file': file}
            )  # Создание файла
            if file_form.is_valid():  # Проверка валидности файла
                news.files.add(file_form.save())  # Добавление нового файла

        return news
