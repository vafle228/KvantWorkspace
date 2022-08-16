from django import forms
from CoreApp.services.m2m import FileM2MBaseMixin
from .models import KvantProject, KvantProjectTask, KvantProjectMembershipRequest
from CoreApp.services.image import ImageThumbnailBaseMixin
from CoreApp.services.filemanager import FileMoveBaseMixin
from CoreApp.services.utils import buildDate
from django.conf import settings


class ProjectPreviewManagerMixin(ImageThumbnailBaseMixin, FileMoveBaseMixin):
    def clean_image(self):
        if not self.errors:
            return self._updateImageValue()
        return self.cleaned_data.get('image')
        
    def _updateImageValue(self):
        if self.instance.image == self.cleaned_data.get('image'):
            return self.changeDirectory(
                self.instance.image,
                f'projects/img/{buildDate(self.instance.date)}/{self.cleaned_data.get("title")}',
                settings.PROJECT_DEFAULT_IMAGE != self.instance.image.name
            )
        return self.makeImageThumbnail(self.cleaned_data.get('image')) 


class KvantProjectTypeSaveForm(forms.ModelForm):
    class Meta:
        model = KvantProjectTask
        fields = ['type',]


class KvantApplicationSaveForm(forms.ModelForm):
    class Meta:
        model = KvantProjectMembershipRequest
        fields = '__all__'


class KvantProjectSaveForm(forms.ModelForm, ProjectPreviewManagerMixin):
    class Meta:
        model = KvantProject
        fields = [ 'title', 'description', 'image']
    
    def __init__(self, *args, **kwargs):
        super(KvantProjectSaveForm, self).__init__(*args, **kwargs)
        super(ProjectPreviewManagerMixin, self).__init__(coef=0.5)
        
        self.fields['title'].error_messages.update({
            'invalid': u'Заголовок невалиден.',
            'required': u'Заголовок не может быть пустым.',
            'max_length': u'Заголовок не может превышать %(limit_value)d (сейчас %(show_value)d).',
        })
        self.fields['image'].error_messages.update({
            'invalid': u'Превью проекта повреждено или не является изображением'
        })


class KvantProjectSubjectSaveForm(forms.ModelForm):
    class Meta:
        model = KvantProject
        fields = ['course_subject', ]


class KvantProjectLeadersSaveForm(forms.ModelForm):
    class Meta:
        model = KvantProject
        fields = ['tutor', 'teamleader', ]


class KvantProjectFilesSaveForm(FileM2MBaseMixin):
    class Meta:
        model = KvantProject
        fields = ['files', ]
    
    def __init__(self, *args, **kwargs):
        super().__init__('files', *args, **kwargs)
    
    def getFileUploadPath(self):
        return f'projects/files/{buildDate(self.instance.date)}/{self.instance.title}'
    
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