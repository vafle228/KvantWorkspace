from django import forms
from .models import FileStorage
from LoginApp.models import KvantUser
from core.mixins import FileManagerMixinBase
from modules.SystemModule.functions import change_file_directory

"""Встроенные формы основанные на модельном предствалении"""

class FileManagerMixin(FileManagerMixinBase):
    def clean_upload_path(self):
        return change_file_directory(self.instance)
    
    def get_from_path(self):
        return self.instance.upload_path
    
    def get_to_path(self):
        return self.cleaned_data.get('upload_path')
    
    def is_file_moveable(self, file):

        file_created = self.instance.pk is None
        file_changed = file == self.cleaned_data.get('file')
        directory_changed = self.get_from_path() != self.get_to_path()
        
        return file_changed and directory_changed and not file_created


class FileStorageSaveForm(forms.ModelForm):
    class Meta:
        model = FileStorage
        fields = '__all__'


class UserThemeChangeForm(forms.ModelForm):
    class Meta:
        model = KvantUser
        fields = ('theme', 'color')
