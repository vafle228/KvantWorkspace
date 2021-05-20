from django import forms
from .models import FileStorage

"""Встроенные формы основанные на модельном предствалении"""


class FileStorageSaveForm(forms.ModelForm):
    class Meta:
        model = FileStorage
        fields = ('file', 'upload_path')
