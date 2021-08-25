from django import forms
from .models import KvantNews


class ImageManagerMixin:
    def clean_image(self):
        from SystemModule.functions import format_image

        file = self.cleaned_data.get('image')
        return self.change_news_image_directory(file) if self.instance.image == file else format_image(file, 0.6)
    
    def change_news_image_directory(self, file):
        from django.utils import timezone
        from SystemModule.functions import change_file_directory
        
        if self.is_image_moveable(file):
            new_image_path = f'news/img/{timezone.now().date()}/{self.cleaned_data.get("title")}'
            from_path = "/".join(self.instance.image.name.split('/')[:-1])
            self.instance.image.name = change_file_directory(file, new_image_path, from_path)
        return file

    def is_image_moveable(self, file):
        from django.conf import settings

        is_file_changed = file == self.instance.image
        is_default_img = settings.NEWS_DEFAULT_IMAGE != self.instance.image.name
        is_directory_changed = self.cleaned_data.get('title') != self.instance.title
        
        return self.cleaned_data.get('title') and is_default_img and is_directory_changed and is_file_changed


class FileManagerMixin:
    def clean_files(self):
        if self.instance.pk is not None:
            self.files_clean_up()
           
            if self.is_file_moveable():
                self.change_news_file_directory()
        return self.cleaned_data['files']
    
    def files_clean_up(self):
        for file in self.instance.files.all():
            if file not in self.cleaned_data['files']:
                file.delete()
    
    def is_file_moveable(self):
        return self.instance.title != self.cleaned_data.get('title') and self.cleaned_data.get('title')
    
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
