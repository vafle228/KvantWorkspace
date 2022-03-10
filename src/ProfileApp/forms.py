from django import forms
from .services import PDFToImageManager
from django.core import validators as v
from os.path import splitext
from .models import KvantAward


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