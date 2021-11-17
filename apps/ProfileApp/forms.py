import fitz
from PIL import Image
from io import BytesIO
from django import forms
from sys import getsizeof
from os.path import splitext
from .models import KvantAward
from core.mixins import ImageMixinBase
from django.core import validators as v
from django.core.files.uploadedfile import InMemoryUploadedFile


class ExtensionAccessManager:
    def __init__(self, file_name):
        self.extension = splitext(file_name)[1][1::]
    
    def is_have_access(self):
        return self.extension == 'pdf' or self.extension in v.get_available_image_extensions()
    
    def is_pdf_file(self):
        return self.extension == 'pdf'
    

class AwardMixin(ImageMixinBase):
    def clean_image(self):
        access_manager = ExtensionAccessManager(self.get_image_file().name)
        
        if not access_manager.is_have_access() :
            raise forms.ValidationError('Загруженный файл не является картинкой или pdf-файлом')
        if access_manager.is_pdf_file():
            self.cleaned_data['image'] = self.convert_pdf_to_image(self.get_image_file())
        return self.image_clean()
    
    def get_image_file(self):
        return self.cleaned_data.get('image')
    
    def get_instance_image(self):
        return self.instance.image
    
    def convert_pdf_to_image(self, pdf_file):
        image = BytesIO()
        document = fitz.open('pdf', pdf_file.read())
        file_name = f'{splitext(pdf_file.name)[0]}.jpeg'

        zoom_matrix = fitz.Matrix(2, 2) # 2 - zoom coefficient
        
        Image.open(BytesIO(document[0].getPixmap(matrix=zoom_matrix).tobytes())).save(image, format='JPEG', quality=90)
        
        return InMemoryUploadedFile(image, 'FileField', file_name, 'image/jpeg', getsizeof(image), None)


class KvantAwardSaveForm(forms.ModelForm, AwardMixin):
    class Meta:
        model = KvantAward
        fields = ('user', 'image')
    
    def __init__(self, *args, **kwargs):      
        super(KvantAwardSaveForm, self).__init__(*args, **kwargs)
        super(AwardMixin, self).__init__(coef=0.65)
    
    def clean_image(self):
        try:
            return super().clean_image()
        except forms.ValidationError as e:
            self.add_error('image', e)