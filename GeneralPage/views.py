from .models import KvantNews
from django.http import JsonResponse
from AdminPage.models import KvantCourse
from django.shortcuts import render, HttpResponse
from LoginPage.models import KvantUser, KvantStudent


def main_page(request, identifier):
    user = KvantUser.objects.filter(id=identifier)[0]  # Получаем пользователя по id
    if user.permission == 'Ученик':  # В случаи, если user - ученик, верни его курсы
        user_course = KvantCourse.objects.filter(students__student=user)  # Получаем все курсы
        return render(request, 'GeneralPage/MainPage/index.html', {'courses': user_course})
    return render(request, 'GeneralPage/MainPage/index.html')


def news_detail_view(request, identifier, news_identifier):
    news = KvantNews.objects.filter(id=news_identifier)[0]  # Получили запрашиваемую новость
    return render(request, 'GeneralPage/NewsView/index.html', {'news': news})


def send_new_news(request):
    if request.method == 'POST':  # Проверка на POST запрос
        news_count = int(request.POST['page']) * 6  # Получаем идекс первой новой новсти
        response = []
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
