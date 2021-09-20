from django import forms
from .models import FileStorage
from LoginApp.models import KvantUser
from core.mixins import FileManagerMixinBase


class FileManagerMixin(FileManagerMixinBase):
    def clean_upload_path(self):
        if self.instance.pk is not None:
            self.change_directory(
                self.cleaned_data.get('file'), 
                self.instance.upload_path, 
                self.cleaned_data.get('upload_path')
            )
        return self.cleaned_data.get('upload_path')
    
    def is_file_moveable(self, file):
        is_file_changed = self.instance.file != file
        is_directory_changed = self.instance.upload_path != self.cleaned_data.get('upload_path')

        return not is_file_changed and is_directory_changed


class FileStorageSaveForm(forms.ModelForm, FileManagerMixin):
    class Meta:
        model = FileStorage
        fields = '__all__'


class UserThemeChangeForm(forms.ModelForm):
    class Meta:
        model = KvantUser
        fields = ('theme', 'color')
