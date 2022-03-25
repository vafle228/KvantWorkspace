from django import forms
from CoreApp.services.m2m import FileM2MBaseMixin
from .models import KvantProject, KvantProjectTask, KvantProjectMembershipRequest


class KvantProjectTypeSaveForm(forms.ModelForm):
    class Meta:
        model = KvantProjectTask
        fields = ['type',]



class KvantApplicationSaveForm(forms.ModelForm):
    class Meta:
        model = KvantProjectMembershipRequest
        fields = '__all__'


class KvantProjectSaveForm(forms.ModelForm):
    class Meta:
        model = KvantProject
        fields = ['tutor', 'title', 'description', 'image', 'teamleader']


class KvantProjectSubjectSaveForm(forms.ModelForm):
    class Meta:
        model = KvantProject
        fields = ['course_subject', ]


class KvantProjectFilesSaveForm(FileM2MBaseMixin):
    class Meta:
        model = KvantProject
        fields = ['files', ]
    
    def __init__(self, *args, **kwargs):
        super().__init__('files', *args, **kwargs)
    
    def getFileUploadPath(self):
        return f'projects/{self.instance.title}'
    
    def clean_files(self):
        """ Отчистка старых файлов """
        for file in self.instance.files.all():
            if file not in self.cleaned_data.get('files'): file.delete() 
        return self.cleaned_data.get('files')


class KvantProjectTaskSaveForm(forms.ModelForm):
    class Meta:
        model = KvantProjectTask
        fields = ['title', 'description', 'deadline', 'priority']


class KvantProjectTaskParticipantsSaveForm(forms.ModelForm):
    class Meta:
        model = KvantProjectTask
        fields = ['participants',]


class KvantProjectTaskFilesSaveForm(FileM2MBaseMixin):
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