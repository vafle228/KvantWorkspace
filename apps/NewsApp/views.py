from .models import KvantNews
from django.utils import timezone
from .forms import KvantNewsSaveForm
from LoginApp.models import KvantUser
from AdminModule.models import KvantCourse
from SystemModule.views import is_available
from django.views.generic.list import ListView
from SystemModule.forms import FileStorageSaveForm
from django.shortcuts import render, HttpResponse, redirect


def main_page(request, identifier):
    # Метод для отображени главной страницы приложения.
    if not is_available(request, identifier):  # Проверка на доступ
        return redirect('/login/')

    # Получаем пользователя по id из url
    max_news = len(KvantNews.objects.all())
    user, user_course = KvantUser.objects.filter(id=identifier)[0], []

    if user.permission == 'Ученик':  # В случаи, если user - ученик, верни его курсы
        user_course = KvantCourse.objects.filter(students__student=user)

    if user.permission == 'Учитель':  # В случаи, если user - учитель, верни его курсы
        user_course = KvantCourse.objects.filter(teacher__teacher=user)
    return render(request, 'NewsApp/MainPage/index.html', {'courses': user_course, 'max_news': max_news})


# Пагинация по новостям
class NewsListView(ListView):
    model               = KvantNews
    ordering            = ['-date']
    paginate_by         = 6
    template_name       = 'NewsApp/NewsPreview/index.html'
    context_object_name = 'all_news'
    
    # Метод делегирования запроса
    def dispatch(self, request, *args, **kwargs):
        user_id = kwargs['identifier']
        if not is_available(request, user_id):  # Проверяем доступ
            return redirect('/login/')
        return super().dispatch(request, *args, **kwargs)  # Исполняем родительский метод


def news_detail_view(request, identifier, news_identifier):
    # Функция просмотра деталей новостей.
    if not is_available(request, identifier):  # Проверка на доступ
        return redirect('/login/')

    if KvantNews.objects.filter(id=news_identifier).exists():  # Проверка существования новости
        news = KvantNews.objects.filter(id=news_identifier)[0]  # Получаем запрашиваемую новость
        return render(request, 'NewsApp/NewsView/index.html', {'news': news})
    return redirect(f'/news/{identifier}/main')


def create_new_news(request, identifier):
    # Функция создает новость на основе формы с FrontEnd.
    if not is_available(request, identifier):  # Проверка на доступ
        return redirect('/login/')

    if request.user.permission == 'Ученик':  # Проверка на права
        return redirect(f'/news/{identifier}/main')

    if request.method == 'POST':  # Проверка метода запроса
        form = KvantNewsSaveForm(request.POST, request.FILES)  # Форма создания новости

        if form.is_valid():
            news = fill_news_files(request, form.save())  # Добавления файлов в новость
            return HttpResponse(f'/news/{request.user.id}/detail/{news.id}')  # Переход на новость
    return HttpResponse(f'/news/{request.user.id}/main')  # Если был неверный метод


# Просто функция для делегирования заполнения новости
def fill_news_files(request, news):
    date = timezone.now().date()
    for file in request.FILES.getlist('files'):  # Добавление файлов в новость
        file_form = FileStorageSaveForm(
            {'upload_path': f'news/files/{date}/{request.POST["title"]}'}, {'file': file}
        )  # Создание файла
        if file_form.is_valid():  # Проверка валидности файла
            news.files.add(file_form.save())  # Добавление нового файла
    return news
