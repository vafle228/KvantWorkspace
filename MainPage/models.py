import PIL
from django.db import models
from gdstorage.storage import GoogleDriveStorage
from django.contrib.auth.models import AbstractUser

gd_storage = GoogleDriveStorage()
permission = (("Ученик", "Ученик"),
              ("Учитель", "Учитель"),
              ("Администратор", "Администратор")
              )


class KvantUser(AbstractUser):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    permission = models.CharField(choices=permission, max_length=100)

    def __str__(self):
        return f'{self.permission} {self.surname} {self.name[0]}.{self.patronymic[0]}'


class FileStorage(models.Model):
    file = models.FileField(upload_to='files', storage=gd_storage)

    def __str__(self):
        return f'Файл {self.file}'


class ImageStorage(models.Model):
    image = models.ImageField(upload_to='images', storage=gd_storage)

    def __str__(self):
        return f'Изображение {self.image}'
