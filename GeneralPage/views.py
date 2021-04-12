from .models import KvantNews
from django.http import JsonResponse
from .forms import KvantNewsSaveForm
from LoginPage.models import KvantUser
from AdminPage.models import KvantCourse
from LoginPage.views import is_available
from django.shortcuts import render, HttpResponse, redirect


def main_page(request, identifier):
    if not is_available(request, identifier):  # Проверка на доступ
        return redirect('/auth/')

    # Получаем пользователя по id из url
    user, user_course = KvantUser.objects.filter(id=identifier)[0], []

    if user.permission == 'Ученик':  # В случаи, если user - ученик, верни его курсы
        user_course = KvantCourse.objects.filter(students__student=user)

    if user.permission == 'Учитель':
        user_course = KvantCourse.objects.filter(teacher__teacher=user)
    return render(request, 'GeneralPage/MainPage/index.html', {'courses': user_course})


def news_detail_view(request, identifier, news_identifier):
    if not is_available(request, identifier):  # Проверка на доступ
        return redirect('/auth/')

    if KvantNews.objects.filter(id=news_identifier).exists():  # Проверка существования новости
        news = KvantNews.objects.filter(id=news_identifier)[0]  # Получили запрашиваемую новость
        return render(request, 'GeneralPage/NewsView/index.html', {'news': news})
    return redirect(f'/general/{identifier}/main')


def send_new_news(request, identifier):
    if not is_available(request, identifier):  # Проверка на доступ
        return redirect('/auth/')

    if request.method == 'POST':  # Проверка на POST запрос
        response = []
        news_count = int(request.POST['page']) * 6  # Получаем идекс первой новой новости
        while len(response) != 6 and news_count < len(KvantNews.objects.all()):  # Перебираем до 6 или конца новостей
            news = KvantNews.objects.all()[news_count]  # Получаем новую новость
            new_news = {
                'id': news.id,
                'title': news.title,
                'content': news.content,
                'image': news.image.image.url,  # Получаем url картинки
            }  # Формирования словаря для json овета
            response.append(new_news)
            news_count += 1
        return JsonResponse({'news': response})
    return HttpResponse('Error')  # Если был отправлен другой запрос


def create_new_news(request, identifier):
    if not is_available(request, identifier):  # Проверка на доступ
        return redirect('/auth/')

    if request.user.permission == 'Ученик':  # Проверка на права
        return redirect(f'/general/{identifier}/main')

    if request.method == 'POST':  # Проверка метода запроса
        form = KvantNewsSaveForm(request.POST)  # Форма создания новости
        news = form.save(request) if form.is_valid() else None  # Попытка создать новость
        return redirect(f'/general/{request.user.id}/news/detail/{news.id}'
                        if news is not None else f'/general/{request.user.id}/main')
    return HttpResponse('Error')  # Если был неверный метод


def test(request):
    return render(request, 'GeneralPage/test.html')
