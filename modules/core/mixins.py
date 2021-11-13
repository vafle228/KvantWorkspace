from abc import abstractmethod
from django.views.generic import View
from LoginApp.models import KvantUser
from django.shortcuts import redirect


class ImageMixinBase:
    def __init__(self, coef):
        self.coef = coef
    
    @abstractmethod
    def get_image_file(self):
        pass

    @abstractmethod
    def get_instance_image(self):
        pass

    def clean_image(self):
        image = self.get_image_file()
        instance_image = self.get_instance_image()

        return instance_image if image == instance_image else self.format_image(image)

    def get_new_size(self, width, height):
        if width > height:
            return (int(width * self.coef), height * int(width * self.coef) // width)
        return (width * int(height * self.coef) // height, int(height * self.coef))
    
    def format_image(self, image_file):
        from PIL import Image
        from io import BytesIO
        from sys import getsizeof
        from django.core.files.uploadedfile import InMemoryUploadedFile

        image = Image.open(image_file)  # Открываем картинку
        new_image = BytesIO()  # Создаем байтовое представление

        image.thumbnail(self.get_new_size(*image.size), resample=Image.ANTIALIAS)  # Делаем миниатюру картинки
        image.convert('RGB').save(new_image, format='JPEG', quality=90)  # Конвертируем в JPEG, ибо мало весит

        file_name = f'{image_file.name.split(".")[0]}.jpeg'

        return InMemoryUploadedFile(new_image, 'ImageField', file_name, 'image/jpeg', getsizeof(new_image), None)
    

class FileManagerMixinBase:
    @abstractmethod
    def is_file_moveable(self, file):
        pass

    def change_directory(self, file, from_path, to_path):
        if self.is_file_moveable(file):
            file.name = self.change_file_directory(file, from_path, to_path)
        return file
    
    def change_file_directory(self, file, from_path, to_path):
        from storages.backends.s3boto3 import S3Boto3Storage
    
        bucket = S3Boto3Storage()
        file_name = file.name.split('/')[-1]
        
        from_path = bucket._normalize_name(bucket._clean_name(f'{from_path}/{file_name}'))
        to_path = bucket._normalize_name(bucket._clean_name(f'{to_path}/{file_name}'))
        
        bucket.connection.meta.client.copy_object(
            Bucket=bucket.bucket_name,
            CopySource=bucket.bucket_name + "/" + from_path,
            Key=to_path)
        bucket.delete(from_path)
        
        return to_path


class KvantJournalAccessMixin(View):
    # Метод делегирования запроса
    def dispatch(self, request, *args, **kwargs):
        from django.urls import reverse_lazy
        
        user_id = kwargs['identifier']
        if not self.is_available(user_id):  # Проверка на доступ
            return redirect(reverse_lazy('login_page'))
        return super().dispatch(request, *args, **kwargs)  # Исполняем родительский метод

    def is_available(self, identifier):
        from django.contrib import messages

        if KvantUser.objects.filter(id=identifier).exists():  # Проверяем существование
            request_user = self.request.user  # Пользователь который запросил
            requested_user = KvantUser.objects.filter(id=identifier)[0]  # Пользовательн которого запросили
            if request_user == requested_user and requested_user.is_authenticated:  # Проверка совпадения
                return True

        # Ошибка в случаи не совпадения или отсутсвия
        messages.error(self.request, 'Отказано в доступе!')
        return False
