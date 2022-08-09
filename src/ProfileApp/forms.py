from os.path import splitext

from CoreApp.services.image import ImageThumbnailBaseMixin
from django import forms
from django.core import validators as v

from .models import KvantAward, SocialInfo
from .services import PDFToImageManager


class KvantAwardPDFToImageManager(PDFToImageManager):
    def clean_image(self):
        if not self.errors:
            return self._manageFile()
        return self.cleaned_data.get('image')
    
    def _manageFile(self):
        ext = splitext(self.cleaned_data['image'].name)[1][1::]
        if self._isValidFile(ext):
            return self.makeImageThumbnail(self.cleaned_data.get('image'))
        raise forms.ValidationError('Загруженный файл не является картинкой или pdf-файлом')
            
    def _isValidFile(self, ext):
        return ext == 'pdf' or ext in v.get_available_image_extensions()


class KvantAwardSaveForm(forms.ModelForm, KvantAwardPDFToImageManager):
    class Meta:
        model = KvantAward
        fields = ['user', 'image']
    
    def __init__(self, *args, **kwargs):
        super(KvantAwardSaveForm, self).__init__(*args, **kwargs)
        super(KvantAwardPDFToImageManager, self).__init__(coef=0.35)
    
    def clean_image(self):
        try:
            return super().clean_image()
        except forms.ValidationError as e:
            self.add_error('image', e)


class SocialInfoBannerImageManager(ImageThumbnailBaseMixin):
    def clean_banner(self):
        if self.instance.banner == self.cleaned_data.get('banner'):
            return self.instance.banner
        return self.makeImageThumbnail(self.cleaned_data.get('banner'))


class SocialInfoBannerSaveForm(forms.ModelForm, SocialInfoBannerImageManager):
    def __init__(self, *args, **kwargs):
        super(SocialInfoBannerSaveForm, self).__init__(*args, **kwargs)
        super(SocialInfoBannerImageManager, self).__init__(coef=0.4)
    
    class Meta:
        model = SocialInfo
        fields = ['banner', ]


class SocialInfoSaveForm(forms.ModelForm):    
    class Meta:
        model = SocialInfo
        fields = ['vk', 'telegram', 'github', 'description',]


class SocialInfoCreateForm(forms.ModelForm, SocialInfoBannerImageManager):
    def __init__(self, *args, **kwargs):
        super(SocialInfoCreateForm, self).__init__(*args, **kwargs)
        super(SocialInfoBannerImageManager, self).__init__(coef=0.4)
    
    class Meta:
        model = SocialInfo
        fields = '__all__'
