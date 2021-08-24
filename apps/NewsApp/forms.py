from django import forms
from .models import KvantNews


class ImageMoveAndThumbnailMixin:
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

        is_default_img = settings.NEWS_DEFAULT_IMAGE != self.instance.image.name
        is_directory_changed = self.cleaned_data.get('title') != self.instance.title
        is_file_changed = file == self.instance.image
        
        return is_default_img and is_directory_changed and is_file_changed


class KvantNewsSaveForm(forms.ModelForm, ImageMoveAndThumbnailMixin):
    class Meta:
        model = KvantNews
        fields = ('title', 'content', 'style_content', 'image', 'author', 'files')
    
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
        return self.instance.title != self.cleaned_data.get('title')
    
    def change_news_file_directory(self):
        from django.utils import timezone
        from SystemModule.forms import FileStorageSaveForm

        new_file_path = f'news/files/{timezone.now().date()}/{self.cleaned_data.get("title")}'
        for file in self.instance.files.all():
            form = FileStorageSaveForm({'upload_path': new_file_path}, instance=file)
            form.save() if form.is_valid() else None

