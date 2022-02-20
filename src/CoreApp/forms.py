from django import forms
from LoginApp.models import KvantUser

from CoreApp.services.filemanager import FileMoveBaseMixin

from .models import FileStorage


class FileManagerMixin(FileMoveBaseMixin):
    """ Рассширение формы для реализации перемещения файлов """
    def clean_file(self):   
        return self.changeDirectory(
            self.cleaned_data.get('file'),
            self.cleaned_data.get('upload_path'),
            self.instance.file == self.cleaned_data.get('file'),
        )


class FileStorageSaveForm(forms.ModelForm, FileManagerMixin):
    class Meta:
        model = FileStorage
        fields = ('upload_path', 'file')
    
    def clean_upload_path(self):
        if not self.cleaned_data.get('upload_path').isprintable():
            raise forms.ValidationError('Путь содержит невалидые символы')
        return self.cleaned_data.get('upload_path')
    


class UserThemeChangeForm(forms.ModelForm):
    class Meta:
        model = KvantUser
        fields = ('theme', 'color')
