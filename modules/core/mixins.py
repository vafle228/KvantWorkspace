from PIL import Image
from io import BytesIO
from sys import getsizeof
from abc import abstractmethod
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from LoginApp.models import KvantUser
from django.views.generic import View
from os.path import basename, join, splitext
from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.uploadedfile import InMemoryUploadedFile


class ImageMixinBase:
    def __init__(self, coef):
        self.coef = coef
    
    @abstractmethod
    def get_image_file(self):
        raise NotImplementedError

    @abstractmethod
    def get_instance_image(self):
        raise NotImplementedError

    def image_clean(self):
        image = self.get_image_file()
        instance_image = self.get_instance_image()

        return instance_image if image == instance_image else self._image_thumbnail(image)

    def _get_new_size(self, width, height):
        if width > height:
            return (int(width * self.coef), height * int(width * self.coef) // width)
        return (width * int(height * self.coef) // height, int(height * self.coef))
    
    def _image_thumbnail(self, image_file):
        image = Image.open(image_file)  # Открываем картинку
        new_image = BytesIO()  # Создаем байтовое представление

        image.thumbnail(self._get_new_size(*image.size), resample=Image.ANTIALIAS)  # Делаем миниатюру картинки
        image.convert('RGB').save(new_image, format='JPEG', quality=90)  # Конвертируем в JPEG, ибо мало весит

        file_name = f'{splitext(image_file.name)[0]}.jpeg'

        return InMemoryUploadedFile(new_image, 'ImageField', file_name, 'image/jpeg', getsizeof(new_image), None)
    

class FileMoveMixinBase:
    @abstractmethod
    def is_file_moveable(self, file):
        raise NotImplementedError
    
    def _get_to_path(self, file, to_path):
        return '/'.join([to_path, basename(file.name)])

    def change_directory(self, file, to_path):
        to_path = self._get_to_path(file, to_path)
        if self.is_file_moveable(file) and file.name != to_path:
            file.name = self._change_file_directory(file, to_path)
        return file
    
    def _change_file_directory(self, file, to_path):
        bucket = S3Boto3Storage()
        
        to_path = bucket._normalize_name(bucket._clean_name(to_path))
        from_path = bucket._normalize_name(bucket._clean_name(file.name))
        
        bucket.connection.meta.client.copy_object(
            Bucket=bucket.bucket_name,
            CopySource=bucket.bucket_name + "/" + from_path,
            Key=to_path)
        bucket.delete(from_path)
        
        return to_path


class KvantJournalAccessMixin(View):
    # Метод делегирования запроса
    def dispatch(self, request, *args, **kwargs):
        user_id = kwargs['identifier']
        if not self._is_available(user_id):  # Проверка на доступ
            return redirect(reverse_lazy('login_page'))
        return super().dispatch(request, *args, **kwargs)  # Исполняем родительский метод

    def _is_available(self, identifier):
        if KvantUser.objects.filter(id=identifier).exists():  # Проверяем существование
            request_user = self.request.user  # Пользователь который запросил
            requested_user = KvantUser.objects.filter(id=identifier)[0]  # Пользовательн которого запросили
            
            if request_user == requested_user and requested_user.is_authenticated:  # Проверка совпадения
                return True

        # Ошибка в случаи не совпадения или отсутсвия
        messages.error(self.request, 'Отказано в доступе!')
        return False
