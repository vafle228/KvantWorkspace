from django import forms
from .models import KvantHomeWork
from CoreApp.services.m2m import FileM2MBaseMixin


class HomeWorkSaveForm(forms.ModelForm):
    class Meta:
        model = KvantHomeWork
        fields = ['text', 'sender']


class HomeWorkFilesSaveForm(FileM2MBaseMixin):
    class Meta:
        model = KvantHomeWork
        fields = ['files', ]
    
    def __init__(self, *args, **kwargs):
        super().__init__('files', *args, **kwargs)

    def getFileUploadPath(self):
        return f'works/{self.instance.sender.username}/work{self.instance.id}'
    
    def clean_files(self):
        """ Отчистка старых файлов """
        for file in self.instance.files.all():
            if file not in self.cleaned_data.get('files'): file.delete() 
        return self.cleaned_data.get('files')
