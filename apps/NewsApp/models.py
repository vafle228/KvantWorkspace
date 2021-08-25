from django.db import models
from django.utils import timezone
from LoginApp.models import KvantUser
from SystemModule.models import FileStorage


def set_default_image():
    from os.path import join
    from django.conf import settings
    from storages.backends.s3boto3 import S3Boto3Storage

    bucket = S3Boto3Storage()
    if not bucket.exists(settings.NEWS_DEFAULT_IMAGE):
        with open(join(settings.MEDIA_ROOT + settings.NEWS_DEFAULT_IMAGE), 'b+r') as f:
            bucket.save(settings.NEWS_DEFAULT_IMAGE, f)
    return settings.NEWS_DEFAULT_IMAGE


def get_path(instance, filename):
    date = timezone.now().date()
    return f'news/img/{date}/{instance.title}/{filename}'



class KvantNews(models.Model):
    content         = models.TextField(blank=True)
    style_content   = models.TextField(blank=True)
    title           = models.CharField(max_length=100)
    date            = models.DateField(default=timezone.now)
    files           = models.ManyToManyField(FileStorage, blank=True)
    author          = models.ForeignKey(KvantUser, on_delete=models.CASCADE)
    image           = models.ImageField(default=set_default_image, upload_to=get_path)

    def __str__(self):
        return f'Новость: {self.title}'
