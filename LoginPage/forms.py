from django import forms
from .models import KvantUser
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class KvantUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = KvantUser
        fields = ('username', 'email', 'password', 'name', 'surname', 'patronymic')


class KvantUserChangeForm(UserChangeForm):
    class Meta:
        model = KvantUser
        fields = ('username', 'email', 'password', 'name', 'surname', 'patronymic')


class KvantUserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150)

    def save(self, request):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if KvantUser.objects.filter(username=username).exists():
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return user
            else:
                messages.error(request, 'Ошибка авторизации! Неверный пароль!')
        else:
            messages.error(request, 'Ошибка авторизации! Неверный логин!')
        return None

