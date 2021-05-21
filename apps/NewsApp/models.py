from PIL import Image
from io import BytesIO
from os.path import join
from sys import getsizeof
from django.db import models
from django.conf import settings
from django.utils import timezone
from LoginApp.models import KvantUser
from SystemModule.models import FileStorage
from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.uploadedfile import InMemoryUploadedFile


def set_default_image():
    bucket = S3Boto3Storage()
    if not bucket.exists('default/news/news.jpg'):
        with open(join(settings.MEDIA_ROOT + '/default/news.jpg'), 'b+r') as f:
            bucket.save('default/news/news.jpg', f)
    return 'default/news/news.jpg'


def get_path(instance, filename):
    date = timezone.now().date()
    return f'news/img/{date}/{instance.title}/{filename}'


class KvantNews(models.Model):
    content = models.TextField(blank=True)
    title = models.CharField(max_length=100)
    style_content = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)
    files = models.ManyToManyField(FileStorage, blank=True)
    author = models.ForeignKey(KvantUser, on_delete=models.CASCADE)
    image = models.ImageField(default=set_default_image, upload_to=get_path)

    class Meta:
        ordering = ['-date', '-id']

    def __str__(self):
        return f'Новость: {self.title}'

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
            getsizeof(new_image), None  # Размер, доп инфа
        )
        # Сохранение через другой save класса
        super(KvantNews, self).save()
