from django.db import models
from django.utils import timezone
from LoginApp.models import KvantUser
from SystemModule.models import FileStorage, ImageStorage


def setDefaultImage():
    """Метод для установки дефолтного изображения"""
    return ImageStorage.objects.filter(upload_path='default/news')[0]


class KvantNews(models.Model):
    content = models.TextField()
    title = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
    files = models.ManyToManyField(FileStorage, blank=True)
    author = models.ForeignKey(KvantUser, on_delete=models.CASCADE)
    image = models.ForeignKey(ImageStorage, default=setDefaultImage,
                              blank=True, on_delete=models.SET(setDefaultImage))

    def __str__(self):
        return f'Новость: {self.title}'
