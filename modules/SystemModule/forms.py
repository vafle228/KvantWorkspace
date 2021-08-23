from django import forms
from .models import FileStorage
from LoginApp.models import KvantUser
from modules.SystemModule.functions import change_file_directory

"""Встроенные формы основанные на модельном предствалении"""


class FileStorageSaveForm(forms.ModelForm):
    class Meta:
        model = FileStorage
        fields = '__all__'
    

    def clean_upload_path(self):
        if self.instance.pk and self.instance.file == self.cleaned_data['file'] and \
            self.instance.upload_path != self.cleaned_data['upload_path']:
            self.instance.file.name = change_file_directory(
                self.instance.file, 
                self.cleaned_data.get('upload_path'),
                self.instance.upload_path
            )
        return self.cleaned_data['upload_path']


class UserThemeChangeForm(forms.ModelForm):
    class Meta:
        model = KvantUser
        fields = ('theme', 'color')
