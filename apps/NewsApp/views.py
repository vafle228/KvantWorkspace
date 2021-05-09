from .models import KvantNews
from django.http import JsonResponse
from .forms import KvantNewsSaveForm
from LoginApp.models import KvantUser
from AdminModule.models import KvantCourse
from SystemModule.views import is_available
from django.shortcuts import render, HttpResponse, redirect


def main_page(request, identifier):
    """
        Метод для отображени главной страницы приложения.
        Интерфейс выдается по permission пользователя из html.
    """
    if not is_available(request, identifier):  # Проверка на доступ
        return redirect('/login/')

    # Получаем пользователя по id из url
    user, user_course = KvantUser.objects.filter(id=identifier)[0], []

    if user.permission == 'Ученик':  # В случаи, если user - ученик, верни его курсы
        user_course = KvantCourse.objects.filter(students__student=user)

    if user.permission == 'Учитель':  # В случаи, если user - учитель, верни его курсы
        user_course = KvantCourse.objects.filter(teacher__teacher=user)
    return render(request, 'NewsApp/MainPage/index.html', {'courses': user_course})


def news_detail_view(request, identifier, news_identifier):
    """
        Функция просмотра деталей новостей.
        Возращает страницу детального просмотра с представлением новости, по ее id
    """
    if not is_available(request, identifier):  # Проверка на доступ
        return redirect('/login/')

    if KvantNews.objects.filter(id=news_identifier).exists():  # Проверка существования новости
        news = KvantNews.objects.filter(id=news_identifier)[0]  # Получили запрашиваемую новость
        return render(request, 'NewsApp/NewsView/index.html', {'news': news})
    return redirect(f'/news/{identifier}/main')


def send_new_news(request, identifier):
    """
        Функция условной пагинации новостей
        Предназначена для ответа на AJAX запрос с FrontEnd
    """
    if not is_available(request, identifier):  # Проверка на доступ
        return redirect('/login/')

    if request.method == 'POST':  # Проверка на POST запрос
        response = []
        news_count = int(request.POST['page']) * 6  # Получаем идекс первой новой новости
        while len(response) != 6 and news_count < len(KvantNews.objects.all()):  # Перебираем до 6 или конца новостей
            news = KvantNews.objects.all()[::-1][news_count]  # Получаем новую новость
            new_news = {
                'id': news.id, 'title': news.title,
                'content': news.content, 'image': news.image.image.url,
            }  # Формирования представления новости
            response.append(new_news)
            news_count += 1
        return JsonResponse({'news': response})
    return HttpResponse('Error')  # Если был отправлен другой запрос


def create_new_news(request, identifier):
    """
        Функция создает новость на основе формы с FrontEnd.
        Для больших подробностей механизма создания смотри forms.py
    """
    if not is_available(request, identifier):  # Проверка на доступ
        return redirect('/login/')

    if request.user.permission == 'Ученик':  # Проверка на права
        return redirect(f'/news/{identifier}/main')

    if request.method == 'POST':  # Проверка метода запроса
        form = KvantNewsSaveForm(request.POST)  # Форма создания новости
        news = form.save(request) if form.is_valid() else None  # Попытка создать новость
        return HttpResponse(f'/news/{request.user.id}/detail/{news.id}'
                            if news is not None else f'/news/{request.user.id}/main')
    return HttpResponse('Error')  # Если был неверный метод

