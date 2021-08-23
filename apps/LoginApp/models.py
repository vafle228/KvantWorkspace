from django.db import models
from django.contrib.auth.models import AbstractUser


PERMISSION = (
    ("Ученик", "Ученик"),
    ("Учитель", "Учитель"),
    ("Администратор", "Администратор")
)

THEME = (
    ("dark", "dark"), 
    ("light", "light")
)

COLOR = (
    ("orange", "orange"), 
    ("blue", "blue")
)


def set_default_image():
    from os.path import join
    from django.conf import settings
    from storages.backends.s3boto3 import S3Boto3Storage

    bucket = S3Boto3Storage()
    if not bucket.exists(settings.USER_DEFAULT_IMAGE):
        with open(join(settings.MEDIA_ROOT + settings.USER_DEFAULT_IMAGE), 'b+r') as f:
            bucket.save(settings.USER_DEFAULT_IMAGE, f)
    return settings.USER_DEFAULT_IMAGE


def get_path(instance, filename):
    return f'user/{instance.username}/{filename}'


class KvantUser(AbstractUser):
    name        = models.CharField(max_length=100)
    surname     = models.CharField(max_length=100)
    patronymic  = models.CharField(max_length=100)
    permission  = models.CharField(choices=PERMISSION, max_length=100)
    color       = models.CharField(max_length=100, choices=COLOR, default='blue')
    theme       = models.CharField(max_length=100, choices=THEME, default='light')
    image       = models.ImageField(upload_to=get_path, default=set_default_image)

    def __str__(self):
        return f'{self.permission} {self.surname} {self.name[0]}.{self.patronymic[0]}.'


class KvantStudent(models.Model):
    student = models.ForeignKey(KvantUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.student.__str__()


class KvantTeacher(models.Model):
    teacher = models.ForeignKey(KvantUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.teacher.__str__()


class KvantAdmin(models.Model):
    admin = models.ForeignKey(KvantUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.admin.__str__()
