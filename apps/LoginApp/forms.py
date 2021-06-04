from django import forms
from .models import KvantUser
from django.contrib import messages
from SystemModule.views import format_image
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class ImageThumbnailFormMixin:
    def clean_image(self):
        file = self.cleaned_data.get('image')  # Получаем картинку

        if self.instance.image == file:  # Если картинка не менялась
            return file

        return format_image(file, 0.3)


class KvantUserCreationForm(UserCreationForm, ImageThumbnailFormMixin):
    class Meta:
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
