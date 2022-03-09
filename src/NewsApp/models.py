from django.db import models
from django.utils import timezone


def setDefaultImage():
    from os.path import join
    from django.conf import settings
    from storages.backends.s3boto3 import S3Boto3Storage

    bucket = S3Boto3Storage()
    if not bucket.exists(settings.NEWS_DEFAULT_IMAGE):
        with open(join(settings.MEDIA_ROOT + settings.NEWS_DEFAULT_IMAGE), 'b+r') as f:
            bucket.save(settings.NEWS_DEFAULT_IMAGE, f)
    return settings.NEWS_DEFAULT_IMAGE


def getPath(instance, filename):
    if not instance.id:
        return f'news/img/{timezone.now().date()}/{instance.title}/{filename}'
    return f'news/img/{instance.date}/{instance.title}/{filename}'


class KvantNews(models.Model):
    content         = models.TextField(blank=True)
    title           = models.CharField(max_length=100)
    date            = models.DateField(default=timezone.now)
    files           = models.ManyToManyField(to='CoreApp.FileStorage', blank=True)
    image           = models.ImageField(default=setDefaultImage, upload_to=getPath)
    author          = models.ForeignKey(to='LoginApp.KvantUser', on_delete=models.CASCADE)

    class Meta:
        db_table = 'kvant_news'

    def __str__(self):
        return f'Новость: {self.title}'