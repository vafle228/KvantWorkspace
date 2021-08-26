import os
from django import forms
from .models import KvantAward
from core.mixins import ImageMixinBase, FileManagerMixinBase


class ExtensionAccessManager:
    def __init__(self, file_name):
        self.extension = os.path.splitext(file_name)[1][1::]
    
    def is_have_access(self):
        from django.core import validators as v

        return self.extension == 'pdf' or self.extension in v.get_available_image_extensions()
    
    def is_pdf_file(self):
        return self.extension == 'pdf'
    

class AwardMixin(ImageMixinBase, FileManagerMixinBase):
    def clean_image(self):
        access_manager = ExtensionAccessManager(self.get_image_file().name)

        if not access_manager.is_have_access() :
            raise forms.ValidationError('Загруженный файл не является картинкой или pdf-файлом')

        if access_manager.is_pdf_file():
            self.cleaned_data['image'] = self.convert_pdf_to_image(self.get_image_file())

        if not self.instance.pk is None:
            to_path = f'portfolio/{self.cleaned_data.get("user").username}'
            from_path = "/".join(self.get_instance_image().name.split('/')[:-1])
            
            return self.change_directory(super().clean_image(), from_path, to_path)
        return super().clean_image()
    
    def get_image_file(self):
        return self.cleaned_data.get('image')
    
    def get_instance_image(self):
        return self.instance.image
    
    def convert_pdf_to_image(self, pdf_file):
        import fitz
        from PIL import Image
        from io import BytesIO
        from sys import getsizeof
        from django.core.files.uploadedfile import InMemoryUploadedFile

        image = BytesIO()
        document = fitz.open('pdf', pdf_file.read())
        file_name = f'{os.path.splitext(pdf_file.name)[0]}.jpeg'
        
        Image.open(BytesIO(document[0].getPixmap(matrix=fitz.Matrix(2, 2)).tobytes())).save(image, format='JPEG', quality=90)
        
        return InMemoryUploadedFile(image, 'FileField', file_name, 'image/jpeg', getsizeof(image), None)
    
    def is_file_moveable(self, file):
        is_file_changed = self.instance.image != file
        is_directory_changed = self.cleaned_data.get('user').username != self.instance.user.username
        
        return is_directory_changed and not is_file_changed

class KvantAwardSaveForm(forms.ModelForm, AwardMixin):
    class Meta:
        model = KvantAward
        fields = ['user', 'image']
    
    def __init__(self, *args, **kwargs):      
        super(KvantAwardSaveForm, self).__init__(*args, **kwargs)
        super(AwardMixin, self).__init__(coef=0.65)