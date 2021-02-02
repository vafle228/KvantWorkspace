from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import KvantUser


class KvantUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = KvantUser
        fields = ('email', 'password', 'name', 'surname', 'patronymic')


class KvantUserChangeForm(UserChangeForm):
    class Meta:
        model = KvantUser
        fields = ('email', 'password', 'name', 'surname', 'patronymic')
