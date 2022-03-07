from django import forms
from .models import KvantTaskBase, KvantTaskMark, KvantHomeTask
from CoreApp.services.m2m import FileM2MBaseMixin


class KvantMarkSaveForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = KvantTaskMark
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['student'].error_messages.update({
            'invalid': u'Выбранный пользователь не существует',
            'required': u'Оценка должна содержать студента для выставления.',
        })


class KvantBaseSaveForm(forms.ModelForm):
    class Meta:
        model = KvantTaskBase
        fields = ['title', 'description']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['title'].error_messages.update({
            'invalid': u'Заголовок невалиден.',
            'required': u'Заголовок не может быть пустым.',
            'max_length': u'Заголовок не может превышать %(limit_value)d (сейчас %(show_value)d).',
        })

    def clean_title(self):
        if not self.cleaned_data.get('title').isprintable():
            raise forms.ValidationError('Заголовок содержит невалидые символы')
        if '/' in self.cleaned_data.get('title'):
            raise forms.ValidationError('Заголовок не может содержать символ "/".')
        return self.cleaned_data.get('title')


class KvantBaseFilesSaveForm(FileM2MBaseMixin):
    class Meta:
        model = KvantTaskBase
        fields = ['files', ]
    
    def __init__(self, *args, **kwargs):
        super().__init__('files', *args, **kwargs)
    
    def clean_files(self):
        """ Отчистка старых файлов """
        for file in self.instance.files.all():
            if file not in self.cleaned_data.get('files'): file.delete() 
        return self.cleaned_data.get('files')


class KvantLessonFilesSaveForm(KvantBaseFilesSaveForm):
    def getFileUploadPath(self):
        return f'lessons/{self.instance.title}'


class KvantTaskFilesSaveForm(KvantBaseFilesSaveForm):
    def getFileUploadPath(self):
        return f'tasks/{self.instance.title}'