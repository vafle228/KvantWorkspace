import PIL
from django.db import models
from gdstorage.storage import GoogleDriveStorage

gd_storage = GoogleDriveStorage()


class FileStorage(models.Model):
    file = models.FileField(upload_to='files', storage=gd_storage)

    def __str__(self):
        return f'Файл {self.file}'


class ImageStorage(models.Model):
    image = models.ImageField(upload_to='images', storage=gd_storage)

    def __str__(self):
        return f'Изображение {self.image}'
