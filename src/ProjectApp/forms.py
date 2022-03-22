from django import forms
from CoreApp.services.m2m import FileM2MBaseMixin
from .models import KvantProjectTask


class KvantProjectSaveForm(forms.ModelForm):
    class Meta:
        model = KvantProjectTask
        fields = ['title', 'description', 'deadline', 'priority']


class KvantProjectParticipantsSaveForm(forms.ModelForm):
    class Meta:
        model = KvantProjectTask
        fields = ['participants',]


class KvantProjectFilesSaveForm(FileM2MBaseMixin):
    class Meta:
        model = KvantProjectTask
        fields = ['files', ]
    
    def __init__(self, *args, **kwargs):
        super().__init__('files', *args, **kwargs)
    
    def getFileUploadPath(self):
        return f'project/tasks/{self.instance.title}'
    
    def clean_files(self):
        """ Отчистка старых файлов """
        for file in self.instance.files.all():
            if file not in self.cleaned_data.get('files'): file.delete() 
        return self.cleaned_data.get('files')