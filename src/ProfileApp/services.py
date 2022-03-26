from io import BytesIO
from os.path import splitext
from sys import getsizeof

import fitz
from CoreApp.services.image import ImageThumbnailBaseMixin
from CoreApp.services.utils import ObjectManipulationManager
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse_lazy as rl
from PIL import Image

from .models import KvantAward


def getUserAwardsQuery(user):
    """ Возвращает все грамоты user """
    return KvantAward.objects.filter(user=user)


class UserChangeManipulationResponse(ObjectManipulationManager):
    def _constructRedirectUrl(self, **kwargs):
        return rl('settings_page')


class PDFToImageManager(ImageThumbnailBaseMixin):
    def __init__(self, coef):
        super().__init__(coef)
    
    def makeImageThumbnail(self, image_file):
        if image_file.content_type == 'application/pdf':
            return super().makeImageThumbnail(self._convertPdfToImage(image_file))
        return super().makeImageThumbnail(image_file)
    
    def _convertPdfToImage(self, pdf_file):
        image = BytesIO()
        document = fitz.open('pdf', pdf_file.read())
        file_name = f'{splitext(pdf_file.name)[0]}.jpeg'

        zoom_matrix = fitz.Matrix(2, 2) # 2 - zoom коэффициент
        byte_pdf = BytesIO(document[0].getPixmap(matrix=zoom_matrix).tobytes())
        
        Image.open(byte_pdf).save(image, format='JPEG', quality=90)
        
        return InMemoryUploadedFile(
            image, 'FileField', file_name, 
            'image/jpeg', getsizeof(image), None
        ) 
    

