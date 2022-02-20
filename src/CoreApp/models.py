from django.db import models


def uploadFile(instance, filename):
    return f'{instance.upload_path}/{filename}'


class FileStorage(models.Model):
    file        = models.FileField(upload_to=uploadFile)
    upload_path = models.TextField(blank=True, default='files/')

    class Meta:
        db_table = 'file_storage'

    def __str__(self):
        return f'Файл: {self.file.name.split("/")[-1]}'
