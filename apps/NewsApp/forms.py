from django import forms
from .models import KvantNews
from django.conf import settings
from SystemModule.models import FileStorage
from django.core.exceptions import ValidationError
from SystemModule.forms import FileStorageSaveForm
from core.mixins import ImageMixinBase, FileMoveMixinBase, ManyToManyObjectCreateMixin


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
    

class KvantNewsSaveForm(forms.ModelForm, ImageManagerMixin):
    class Meta:
        model = KvantNews
        fields = ['title', 'content', 'image', 'author']
    
    def __init__(self, *args, **kwargs):
        super(KvantNewsSaveForm, self).__init__(*args, **kwargs)
        super(ImageManagerMixin, self).__init__(coef=0.7)
        
        self.fields['title'].error_messages.update({
            'invalid': u'Заголовок невалиден.',
            'required': u'Заголовок не может быть пустым.',
            'max_length': u'Заголовок не может превышать %(limit_value)d (сейчас %(show_value)d).',
        })
        self.fields['image'].error_messages.update({
            'invalid': u'Превью новости повреждено или не является изображением'
        })

    def clean_title(self):
        if not self.cleaned_data.get('title').isprintable():
            raise forms.ValidationError('Заголовок содержит невалидые символы')
        if '/' in self.cleaned_data.get('title'):
            raise forms.ValidationError('Заголовок не может содержать символ "/".')
        return self.cleaned_data.get('title')


class KvantNewsFilesSaveForm(ManyToManyObjectCreateMixin):
    class Meta:
        model = KvantNews
        fields = ['files', ]

    def __init__(self, *args, **kwargs):
        super().__init__('files', *args, **kwargs)

        self.fields['files'].error_messages.update({
            'max_upload_count': u'Объект не может содеражть более 16 файлов',
            'max_upload_weight': u'Суммарный объем файлов не может превышать 32mB.',
        })
    
    def get_data(self):
        if self.cleaned_data.get('files'):
            return self.files.getlist('files') + list(self.cleaned_data['files'])
        return self.files.getlist('files')

    def validate_value(self, values):
        if len(values) > 16:
            raise ValidationError(self.fields['files'].error_messages['max_upload_count'])
        size_count = 0
        for file in values:
            size_count += file.file.size if isinstance(file, FileStorage) else file.size

            if size_count > 32 * 1024 * 1024:
                raise ValidationError(self.fields['files'].error_messages['max_upload_weight'])

    def create_objects(self, values):
        news_files = []
        for file in values:
            if isinstance(file, FileStorage):
                form = FileStorageSaveForm(
                    {'upload_path': f'news/files/{self.instance.date}/{self.instance.title}'}, instance=file
                )
            else:
                form = FileStorageSaveForm(
                    {'upload_path': f'news/files/{self.instance.date}/{self.instance.title}'}, {'file': file}
                )
            news_files.append(str(form.save().id)) if form.is_valid() else None
        return news_files
    
    def clean_files(self):
        for file in self.instance.files.all():
            file.delete() if file not in self.cleaned_data.get('files') else None
        return self.cleaned_data.get('files')