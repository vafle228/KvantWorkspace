from django import forms
from .models import KvantNews
from SystemModule.views import format_image


class ImageThumbnailFormMixin:
    def clean_image(self):
        file = self.cleaned_data.get('image')  # Получаем картинку

        if self.instance.image == file:  # Если картинка не менялась
            return file

        return format_image(file, 0.6)


class KvantNewsSaveForm(forms.ModelForm, ImageThumbnailFormMixin):
    class Meta:
        model = KvantNews
        fields = ('title', 'content', 'style_content', 'image', 'author', 'files')


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
