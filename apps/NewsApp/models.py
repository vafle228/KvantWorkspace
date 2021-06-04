from os.path import join
from django.db import models
from django.conf import settings
from django.utils import timezone
from LoginApp.models import KvantUser
from SystemModule.models import FileStorage
from storages.backends.s3boto3 import S3Boto3Storage


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
