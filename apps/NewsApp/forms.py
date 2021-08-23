from django import forms
from .models import KvantNews


class ImageMoveAndThumbnailMixin:
    def clean_image(self):
        from django.conf import settings
        from django.utils import timezone
        from SystemModule.functions import format_image, change_file_directory

        file = self.cleaned_data.get('image')  # Получаем картинку
        if file == self.instance.image and self.cleaned_data.get('title') != self.instance.title:
            if settings.NEWS_DEFAULT_IMAGE != self.instance.image.name:
                new_image_path = f'news/img/{timezone.now().date()}/{self.cleaned_data.get("title")}'
                from_path = "/".join(self.instance.image.name.split('/')[:-1])
                self.instance.image.name = change_file_directory(file, new_image_path, from_path)
        # Если картинка не менялась, то не обрабатываем ее
        return file if self.instance.image == file else format_image(file, 0.6)


class KvantNewsSaveForm(forms.ModelForm, ImageMoveAndThumbnailMixin):
    class Meta:
        model = KvantNews
        fields = ('title', 'content', 'style_content', 'image', 'author', 'files')
    
    def clean_files(self):
        from django.utils import timezone
        from SystemModule.forms import FileStorageSaveForm

        if self.instance.pk is not None:
            for file in self.instance.files.all():
                if file not in self.cleaned_data['files']:
                    file.delete()
           
            if self.instance.title != self.cleaned_data.get('title'):
                new_file_path = f'news/files/{timezone.now().date()}/{self.cleaned_data.get("title")}'
                for file in self.instance.files.all():
                    form = FileStorageSaveForm({'upload_path': new_file_path}, instance=file)
                    form.save() if form.is_valid() else None
        return self.cleaned_data['files']
