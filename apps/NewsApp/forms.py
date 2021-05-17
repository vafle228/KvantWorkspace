from django import forms
from .models import KvantNews
from django.utils import timezone
from SystemModule.forms import ImageStorageSaveForm, FileStorageSaveForm


class KvantNewsSaveForm(forms.Form):
    content = forms.CharField()
    style_content = forms.CharField()
    title = forms.CharField(max_length=100)

    def save(self, request):
        #  Считываем данные с запроса
        date = timezone.now().date()
        title = self.cleaned_data['title']
        content = self.cleaned_data['content']
        style_content = self.cleaned_data['style_content']

        news = KvantNews.objects.create(
            content=content, author=request.user,
            title=title, style_content=style_content,
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


class SendNewNews(forms.Form):
    page = forms.IntegerField()

    def save(self):
        response = []  # Массив объектов новости
        news_count = self.cleaned_data['page'] * 6  # Получаем идекс первой новой новости
        while len(response) != 6 and news_count < len(KvantNews.objects.all()):
            # Перебираем до 6 или конца новостей
            news = KvantNews.objects.all()[::-1][news_count]  # Получаем новую новость
            author = {
                'name': ' '.join(news.author.__str__().split(' ')[1::]),
                'img': news.author.image.image.url
            }  # Объект пользователя
            news_date = '.'.join(news.date.__str__().split('-')[::-1])  # Формат даты
            new_news = {
                'id': news.id, 'title': news.title, 'author': author,
                'content': news.content, 'image': news.image.image.url, 'date': news_date,
            }  # Формирования представления новости
            news_count += 1
            response.append(new_news)
        return response
