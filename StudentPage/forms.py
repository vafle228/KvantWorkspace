from django import forms
from .models import FileStorage, ImageStorage


class FileStorageSaveForm(forms.ModelForm):
    class Meta:
        model = FileStorage
        fields = ('file', 'upload_path')


class ImageStorageSaveForm(forms.ModelForm):
    class Meta:
        model = ImageStorage
        fields = ('image', 'upload_path')
