import sys
from PIL import Image
from io import BytesIO
from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile


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

    def save(self, *args, **kwargs):
        image = Image.open(self.image)  # Открываем картинку
        width, height = image.size  # Получаем размеры картинки
        new_image = BytesIO()  # Создаем байтовое представление

        resize = (width * (height // 10 * 6) // height, height // 10 * 6)  # Изменение по высоте

        if width > height:  # Если горизонтальная картинка
            resize = (width // 10 * 6, height * (width // 10 * 6) // width)  # Изменение по ширине

        image.thumbnail(resize, resample=Image.ANTIALIAS)  # Делаем миниатюру картинки
        image = image.convert('RGB')  # Убираем все лишние каналы
        image.save(new_image, format='JPEG', quality=90)  # Конвертируем в JPEG, ибо мало весит

        new_image.seek(0)  # Возвращение в начало файла

        name = f'{self.image.name.split(".")[0]}.jpeg'  # Имя файла

        # Перезапись файла в базе данных
        self.image = InMemoryUploadedFile(
            new_image, 'ImageField',  # Картинка, поля сохранения
            name, 'image/jpeg',  # Имя картинки, содержание
            sys.getsizeof(new_image), None  # Размер, доп инфа
        )

        # Сохранение через другой save класса
        super(ImageStorage, self).save()
