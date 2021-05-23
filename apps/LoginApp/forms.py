from PIL import Image
from io import BytesIO
from django import forms
from sys import getsizeof
from .models import KvantUser
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class ImageThumbnailFormMixin:
    def clean_image(self):
        file = self.cleaned_data.get('image')  # Получаем картинку

        if self.instance.image == file:  # Если картинка не менялась
            return file

        image = Image.open(file)  # Открываем картинку
        width, height = image.size  # Получаем размеры картинки
        new_image = BytesIO()  # Создаем байтовое представление

        resize = (width * (height // 10 * 3) // height, height // 10 * 3)  # Изменение по высоте

        if width > height:  # Если горизонтальная картинка
            resize = (width // 10 * 3, height * (width // 10 * 3) // width)  # Изменение по ширине

        image.thumbnail(resize, resample=Image.ANTIALIAS)  # Делаем миниатюру картинки
        image = image.convert('RGB')  # Убираем все лишние каналы
        image.save(new_image, format='JPEG', quality=90)  # Конвертируем в JPEG, ибо мало весит

        new_image.seek(0)  # Возвращение в начало файла

        name = f'{file.name.split(".")[0]}.jpeg'  # Имя файла

        # Перезапись файла в базе данных
        model_image = InMemoryUploadedFile(
            new_image, 'ImageField',  # Картинка, поля сохранения
            name, 'image/jpeg',  # Имя картинки, содержание
            getsizeof(new_image), None  # Размер, доп инфа
        )
        # Сохранение через другой save класса
        return model_image


class KvantUserCreationForm(UserCreationForm, ImageThumbnailFormMixin):
    class Meta(UserCreationForm):
        model = KvantUser
        fields = ('username', 'email', 'password', 'name', 'surname', 'patronymic', 'image')


class KvantUserChangeForm(UserChangeForm, ImageThumbnailFormMixin):
    class Meta:
        model = KvantUser
        fields = ('username', 'email', 'password', 'name', 'surname', 'patronymic', 'image')


class KvantUserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150)

    def save(self, request):
        username = self.cleaned_data['username']  # Получение логина
        password = self.cleaned_data['password']  # Получение пароля

        if KvantUser.objects.filter(username=username).exists():  # Проверка существования акаунта
            user = authenticate(username=username, password=password)  # Попытка авторизации
            if user is not None:  # Если попытка удачна, то авторизуй и верни пользователя
                login(request, user)
                return user
        messages.error(request, 'Ошибка авторизации!')  # Сообщение об ощибки
        return None
