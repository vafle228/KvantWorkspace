from django import forms
from .models import KvantUser
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class KvantUserCreationForm(UserCreationForm):
    """
        Переопределение формы создания User.
        Нужена для админ панели
    """
    class Meta(UserCreationForm):
        model = KvantUser
        fields = ('username', 'email', 'password', 'name', 'surname', 'patronymic')


class KvantUserChangeForm(UserChangeForm):
    """
        Переопределение формы изменения User.
        Нужна для админ панели
    """
    class Meta:
        model = KvantUser
        fields = ('username', 'email', 'password', 'name', 'surname', 'patronymic')


class KvantUserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150)

    def save(self, request):
        """
            Авторизация проходит через попытку авторизации пользователя встроенными методами
            В случаи неудачной попытки или отсутвия акаунта, будет выслано оповещение об этом
        """
        username = self.cleaned_data['username']  # Получение логина
        password = self.cleaned_data['password']  # Получение пароля

        if KvantUser.objects.filter(username=username).exists():  # Проверка существования акаунта
            user = authenticate(username=username, password=password)  # Попытка авторизации
            if user is not None:  # Если попытка удачна, то авторизуй и верни пользователя
                login(request, user)
                return user
        messages.error(request, 'Ошибка авторизации!')  # Сообщение об ощибки
        return None
