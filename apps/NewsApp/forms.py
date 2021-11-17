from django import forms
from .models import KvantNews
from django.conf import settings
from SystemModule.forms import FileStorageSaveForm
from core.mixins import ImageMixinBase, FileMoveMixinBase


class ImageManagerMixin(ImageMixinBase, FileMoveMixinBase):
    def clean_image(self):
        return self.change_directory(
            self.image_clean(), 
            f'news/img/{self.instance.date}/{self.cleaned_data.get("title")}'
        )

    def get_image_file(self):
        return self.cleaned_data.get('image')
    
    def get_instance_image(self):
        return self.instance.image
    
    def is_file_moveable(self, file):
        is_file_changed = file != self.cleaned_data.get('image')
        is_default_img = settings.NEWS_DEFAULT_IMAGE == file.name
        
        return not is_default_img and not is_file_changed


class FileManagerMixin:
    def clean_files(self):
        if self.instance.pk is not None:
            self.files_clean_up()
           
            if self.cleaned_data.get('title') is not None:
                self.change_news_file_directory()
        return self.cleaned_data.get('files')
    
    def files_clean_up(self):
        for file in self.instance.files.all():
            file.delete() if file not in self.cleaned_data.get('files') else None
    
    def change_news_file_directory(self):
        new_file_path = f'news/files/{self.instance.date}/{self.cleaned_data.get("title")}'
        for file in self.instance.files.all():
            form = FileStorageSaveForm({'upload_path': new_file_path}, instance=file)
            form.save() if form.is_valid() else None
    

class KvantNewsSaveForm(forms.ModelForm, ImageManagerMixin, FileManagerMixin):
    class Meta:
        model = KvantNews
        fields = ['title', 'content', 'image', 'author', 'files']
    
    def __init__(self, *args, **kwargs):
        super(KvantNewsSaveForm, self).__init__(*args, **kwargs)
        super(ImageManagerMixin, self).__init__(coef=0.7)
        
        self.fields['title'].error_messages.update({
            'invalid': u'Заголовок невалиден.',
            'required': u'Заголовок не может быть пустым.',
            'max_length': u'Заголовок не может превышать %(max)d (сейчас %(length)d).',
        })
        self.fields['image'].error_messages.update({
            'invalid': u'Превью новости повреждено или не является изображением'
        })

    def clean_title(self):
        if not self.cleaned_data.get('title').isprintable():
            raise forms.ValidationError('Заголовок содержит невалидые символы')
        if '/' in self.cleaned_data.get('title'):
            raise forms.ValidationError('Заголовок не может содержать "/" символ')
        return self.cleaned_data.get('title')
