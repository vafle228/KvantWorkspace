from django import forms
from .models import KvantNews
from core.mixins import ImageMixinBase, FileManagerMixinBase


class ImageManagerMixin(ImageMixinBase, FileManagerMixinBase):
    def clean_image(self):
        from django.utils import timezone
        
        from_path = "/".join(self.get_instance_image().name.split('/')[:-1])
        to_path = f'news/img/{timezone.now().date()}/{self.cleaned_data.get("title")}'
        
        return self.change_directory(super().clean_image(), from_path, to_path)

    def get_image_file(self):
        return self.cleaned_data.get('image')
    
    def get_instance_image(self):
        return self.instance.image
    
    def is_file_moveable(self, file):
        from django.conf import settings

        is_file_changed = file != self.cleaned_data.get('image')
        is_default_img = settings.NEWS_DEFAULT_IMAGE == file.name
        is_directory_changed = self.cleaned_data.get('title') != self.instance.title
        
        return self.cleaned_data.get('title') and not is_default_img and is_directory_changed and not is_file_changed


class FileManagerMixin:
    def clean_files(self):
        if self.instance.pk is not None:
            self.files_clean_up()
           
            if self.cleaned_data.get('title') is not None:
                self.change_news_file_directory()
        return self.cleaned_data.get('files')
    
    def files_clean_up(self):
        for file in self.instance.files.all():
            if file not in self.cleaned_data.get('files'):
                file.delete()
    
    def change_news_file_directory(self):
        from django.utils import timezone
        from SystemModule.forms import FileStorageSaveForm

        new_file_path = f'news/files/{timezone.now().date()}/{self.cleaned_data.get("title")}'
        for file in self.instance.files.all():
            form = FileStorageSaveForm({'upload_path': new_file_path}, instance=file)
            form.save() if form.is_valid() else None
    

class KvantNewsSaveForm(forms.ModelForm, ImageManagerMixin, FileManagerMixin):
    class Meta:
        model = KvantNews
        fields = ['title', 'content', 'style_content', 'image', 'author', 'files']
    
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
        if not self.cleaned_data.get('title').strip():
            raise forms.ValidationError('Заголовок не может быть пустым. Заголовок невалиден')
        if not self.cleaned_data.get('title').isprintable():
            raise forms.ValidationError('Заголовок содержит невалидые символы')
        if '/' in self.cleaned_data.get('title'):
            raise forms.ValidationError('Заголовок не может содержать "/" символ')
        return self.cleaned_data['title'] 
