from django import forms
from .models import KvantUser
from core.mixins import ImageMixinBase
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class ImageManagerMixin(ImageMixinBase):
    def clean_image(self):
        return self.image_clean()
    
    def get_image_file(self):
        return self.cleaned_data.get('image')
    
    def get_instance_image(self):
        return self.instance.image


class KvantUserCreationForm(UserCreationForm, ImageManagerMixin):
    def __init__(self, *args, **kwargs):
        super(KvantUserCreationForm, self).__init__(*args, **kwargs)
        super(ImageManagerMixin, self).__init__(coef=0.35)
    
    class Meta:
        model = KvantUser
        fields = ('username', 'email', 'password', 'name', 'surname', 'patronymic', 'image')


class KvantUserChangeForm(UserChangeForm, ImageManagerMixin):
    def __init__(self, *args, **kwargs):
        super(KvantUserChangeForm, self).__init__(*args, **kwargs)
        super(ImageManagerMixin, self).__init__(coef=0.4)
    
    class Meta:
        model = KvantUser
        fields = ('username', 'email', 'password', 'name', 'surname', 'patronymic', 'image')


class KvantUserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150)

    def save(self, request):
        from django.contrib import messages
        from django.contrib.auth import login, authenticate

        username = self.cleaned_data['username']  # Получение логина
        password = self.cleaned_data['password']  # Получение пароля

        if KvantUser.objects.filter(username=username).exists():  # Проверка существования акаунта
            user = authenticate(username=username, password=password)  # Попытка авторизации
            if user is not None:  # Если попытка удачна, то авторизуй и верни пользователя
                login(request, user)
                return user
        messages.error(request, 'Ошибка авторизации!')  # Сообщение об ощибки
        return None
