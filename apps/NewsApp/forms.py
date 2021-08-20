from django import forms
from .models import KvantNews
from django.core import serializers
from SystemModule.views import format_image


class ImageThumbnailFormMixin:
    def clean_image(self):
        file = self.cleaned_data.get('image')  # Получаем картинку

        if self.instance.image == file:  # Если картинка не менялась
            return file

        return format_image(file, 0.6)


class KvantNewsSaveForm(forms.ModelForm, ImageThumbnailFormMixin):
    class Meta:
        model = KvantNews
        fields = ('title', 'content', 'style_content', 'image', 'author', 'files')
