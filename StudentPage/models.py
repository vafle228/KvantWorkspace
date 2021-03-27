from django.db import models


def uploadFile(instance, filename):
    return f'{instance.upload_path}/{filename}'


class FileStorage(models.Model):
    file = models.FileField(upload_to=uploadFile)
    upload_path = models.TextField(blank=True, default='files/')

    def __str__(self):
        return f'Файл {self.file.name.split("/")[-1]}'


class ImageStorage(models.Model):
    image = models.ImageField(upload_to=uploadFile)
    upload_path = models.TextField(blank=True, default='images/')

    def __str__(self):
        return f'Изображение {self.image.name.split("/")[-1]}'
