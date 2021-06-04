from PIL import Image
from io import BytesIO
from sys import getsizeof
from django.contrib import messages
from LoginApp.models import KvantUser
from django.contrib.auth import logout
from django.shortcuts import redirect, HttpResponse
from django.core.files.uploadedfile import InMemoryUploadedFile


def is_available(request, identifier):
    if KvantUser.objects.filter(id=identifier).exists():  # Проверяем существование
        request_user = request.user  # Пользователь который запросил
        requested_user = KvantUser.objects.filter(id=identifier)[0]  # Пользовательн которого запросили
        if request_user == requested_user and requested_user.is_authenticated:  # Проверка совпадения
            return True

    # Ошибка в случаи не совпадения или отсутсвия
    messages.error(request, 'Отказано в доступе!')
    return False


def logout_user(request, identifier):
    if not is_available(request, identifier):
        return redirect('/login/')
    logout(request)
    return redirect('/login/')


def change_user_theme(request, identifier):
    if not is_available(request, identifier):  # Проверка на доступ
        return redirect('/login/')

    if request.method == 'POST':  # Проверка на POST запрос
        user = KvantUser.objects.filter(id=identifier)[0]  # Получаем пользователя

        user.theme = request.POST['theme']  # Перезаписываем тему
        user.color = request.POST['color']  # Перезаписываем цвет

        user.save()  # Сохраняем изменения
        return HttpResponse('OK')  # Бесполезный ответ
    return HttpResponse('Error')  # Если был не POST запрос или запрет


def format_image(image_file, coefficient):
    image = Image.open(image_file)  # Открываем картинку
    width, height = image.size  # Получаем размеры картинки
    new_image = BytesIO()  # Создаем байтовое представление

    resize = (width * int(height * coefficient) // height, int(height * coefficient))  # Изменение по высоте

    if width > height:  # Если горизонтальная картинка
        resize = (int(width * coefficient), height * int(width * coefficient) // width)  # Изменение по ширине

    image.thumbnail(resize, resample=Image.ANTIALIAS)  # Делаем миниатюру картинки
    image = image.convert('RGB')  # Убираем все лишние каналы
    image.save(new_image, format='JPEG', quality=90)  # Конвертируем в JPEG, ибо мало весит

    new_image.seek(0)  # Возвращение в начало файла

    name = f'{image_file.name.split(".")[0]}.jpeg'  # Имя файла

    # Перезапись файла в базе данных
    model_image = InMemoryUploadedFile(
        new_image, 'ImageField',  # Картинка, поля сохранения
        name, 'image/jpeg',  # Имя картинки, содержание
        getsizeof(new_image), None  # Размер, доп инфа
    )
    return model_image
