from email.policy import default
from django.db import models


def get_path(instance, filename):
    return f'portfolio/{instance.user.username}/{filename}'


class KvantAward(models.Model):
    image = models.FileField(upload_to=get_path)
    user = models.ForeignKey(to='LoginApp.KvantUser', on_delete=models.CASCADE)

    class Meta:
        db_table = 'kvant_awards'

    def __str__(self):
        return f'Грамота: {self.user}'


def set_default_image():
    from os.path import join
    from django.conf import settings
    from storages.backends.s3boto3 import S3Boto3Storage

    bucket = S3Boto3Storage()
    if not bucket.exists(settings.USER_BANNER_DEFAULT_IMAGE):
        with open(join(settings.MEDIA_ROOT + settings.USER_BANNER_DEFAULT_IMAGE), 'b+r') as f:
            bucket.save(settings.USER_BANNER_DEFAULT_IMAGE, f)
    return settings.USER_BANNER_DEFAULT_IMAGE


def get_banner_path(instance, filename):
    return f'user/{instance.user.username}/{filename}' 


class SocialInfo(models.Model):
    description = models.TextField(blank=True)
    vk          = models.CharField(max_length=255, blank=True)
    telegram    = models.CharField(max_length=255, blank=True)
    github      = models.CharField(max_length=255, blank=True)
    banner      = models.ImageField(default=set_default_image, upload_to=get_banner_path)
    
    user        = models.OneToOneField(to="LoginApp.KvantUser", on_delete=models.CASCADE)