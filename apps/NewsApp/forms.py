from django import forms
from .models import KvantNews
from django.utils import timezone
from SystemModule.forms import FileStorageSaveForm


class KvantNewsSaveForm(forms.Form):
    content = forms.CharField()
    style_content = forms.CharField()
    title = forms.CharField(max_length=100)

    def save(self, request):
        date = timezone.now().date()  # Дата новости

        news = KvantNews.objects.create(
            style_content=self.cleaned_data['style_content'],
            title=self.cleaned_data['title'], author=request.user,
            image=request.FILES['image'], content=self.cleaned_data['content'],
        )  # Создание новости

        for file in request.FILES.getlist('files'):  # Добавление файлов в новость
            file_form = FileStorageSaveForm(
                {'upload_path': f'news/files/{date}/{news.title}'}, {'file': file}
            )  # Создание файла
            if file_form.is_valid():  # Проверка валидности файла
                news.files.add(file_form.save())  # Добавление нового файла

        return news


class SendNewNews(forms.Form):
    page = forms.IntegerField()

    def save(self):
        response = []  # Массив объектов новости
        news_count = self.cleaned_data['page'] * 6  # Получаем идекс первой новой новости

        # Перебираем до 6 или конца новостей
        while len(response) != 6 and news_count < len(KvantNews.objects.all()):
            news = KvantNews.objects.all()[news_count]  # Получаем новую новость

            author = {
                'img': news.author.image.url,
                'name': ' '.join(news.author.__str__().split(' ')[1::]),
            }  # Объект пользователя
            news_date = '.'.join(news.date.__str__().split('-')[::-1])  # Формат даты

            new_news = {
                'id': news.id, 'title': news.title, 'author': author,
                'content': news.content, 'image': news.image.url, 'date': news_date,
            }  # Формирования представления новости
            news_count += 1
            response.append(new_news)
        return response
