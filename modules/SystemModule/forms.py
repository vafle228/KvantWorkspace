from django import forms
from .models import FileStorage
from LoginApp.models import KvantUser
from core.mixins import FileMoveMixinBase


class FileManagerMixin(FileMoveMixinBase):
    def clean_file(self):
        if self.instance.pk is not None:
            self.change_directory(
                self.cleaned_data.get('file'), 
                self.cleaned_data.get('upload_path'),
            )
        return self.cleaned_data.get('file')
    
    def is_file_moveable(self, file):
        return self.instance.file == file


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
