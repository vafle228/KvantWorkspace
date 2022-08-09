from io import BytesIO
from os.path import splitext
from sys import getsizeof

import fitz
from CoreApp.services.access import KvantObjectExistsMixin
from CoreApp.services.image import ImageThumbnailBaseMixin
from CoreApp.services.utils import ObjectManipulationManager
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse_lazy as rl
from LoginApp.models import KvantUser
from LoginApp.services import getUserById
from PIL import Image

from .models import KvantAward


def getUserAwardsQuery(user):
    """ Возвращает все грамоты user """
    return KvantAward.objects.filter(user=user)


class UserManipulationManager(ObjectManipulationManager):
    def updateUserObj(self, request, user):
        obj_or_errors = self._getUpdatedObject(request)
        return self.getResponse(obj_or_errors, user=user)
    
    def _constructRedirectUrl(self, **kwargs):
        return rl('settings_page', kwargs={'user_identifier': kwargs.get('user').id})


class PortfolioManipulationManager(ObjectManipulationManager):
    def createPortfolioInstance(self, request):
        user_id = request.POST.get('user')
        return self.getResponse(self._getCreatedObject(request), user_id=user_id)
    
    def _constructRedirectUrl(self, **kwargs):
        return rl('portfolio_page', kwargs={'user_identifier': kwargs.get('user_id')})


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
    

class UserExistsMixin(KvantObjectExistsMixin):
    request_object_arg = 'user_identifier'

    def _objectExiststTest(self, object_id):
        return KvantUser.objects.filter(id=object_id).exists()


class UserManipulationMixin(UserExistsMixin):
    def accessTest(self, **kwargs):
        if super().accessTest(**kwargs):
            requested_user = getUserById(kwargs.get(self.request_object_arg))
            return self._profileAccessTest(kwargs.get('user'), requested_user)
        return False
    
    def _profileAccessTest(self, user, requested_user):
        return user == requested_user or user.permission != 'Ученик'
