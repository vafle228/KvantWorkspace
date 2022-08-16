from CoreApp.services.filemanager import FileMoveBaseMixin
from CoreApp.services.image import ImageThumbnailBaseMixin
from CoreApp.services.m2m import FileM2MBaseMixin
from CoreApp.services.utils import buildDate
from django import forms
from django.conf import settings

from .models import KvantNews


class ImageManagerMixin(ImageThumbnailBaseMixin, FileMoveBaseMixin):
    """ Рассширение для реализации урезки превью """
    def clean_image(self):
        if not self.errors:
            return self._updateImageValue()
        return self.cleaned_data.get('image')
        
    def _updateImageValue(self):
        if self.instance.image == self.cleaned_data.get('image'):
            return self.changeDirectory(
                self.instance.image, 
                f'news/img/{buildDate(self.instance.date)}/{self.cleaned_data.get("title")}',
                settings.NEWS_DEFAULT_IMAGE != self.instance.image.name
            )
        return self.makeImageThumbnail(self.cleaned_data.get('image'))  
    

class KvantNewsSaveForm(forms.ModelForm, ImageManagerMixin):
    class Meta:
        model = KvantNews
        fields = ['title', 'content', 'image', 'author', 'is_event']
    
    def __init__(self, *args, **kwargs):
        super(KvantNewsSaveForm, self).__init__(*args, **kwargs)
        super(ImageManagerMixin, self).__init__(coef=0.6)
        
        self.fields['title'].error_messages.update({
            'invalid': u'Заголовок невалиден.',
            'required': u'Заголовок не может быть пустым.',
            'max_length': u'Заголовок не может превышать %(limit_value)d (сейчас %(show_value)d).',
        })
        self.fields['image'].error_messages.update({
            'invalid': u'Превью новости повреждено или не является изображением'
        })
    
    def clean_is_event(self):
        return self.instance.is_event

    def clean_title(self):
        if not self.cleaned_data.get('title').isprintable():
            raise forms.ValidationError('Заголовок содержит невалидые символы')
        if '/' in self.cleaned_data.get('title'):
            raise forms.ValidationError('Заголовок не может содержать символ "/".')
        return self.cleaned_data.get('title')


class KvantNewsFilesSaveForm(FileM2MBaseMixin):
    class Meta:
        model = KvantNews
        fields = ['files', ]

    def __init__(self, *args, **kwargs):
        super().__init__('files', *args, **kwargs)
        
    def getFileUploadPath(self):
        return f'news/files/{buildDate(self.instance.date)}/{self.instance.title}'

    def clean_files(self):
        """ Отчистка старых файлов """
        for file in self.instance.files.all():
            if file not in self.cleaned_data.get('files'): file.delete() 
        return self.cleaned_data.get('files')
