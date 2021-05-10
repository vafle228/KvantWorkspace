from django.db import models
from django.contrib.auth.models import AbstractUser
from SystemModule.models import ImageStorage

permission = (
    ("Ученик", "Ученик"),
    ("Учитель", "Учитель"),
    ("Администратор", "Администратор")
)

theme = (("Темная", "dark"), ("Светлая", "light"))

color = (("Оранжевый", "orange"), ("Синий", "blue"))


def set_default_image():
    """Метод для установки дефолтного изображения"""
    return ImageStorage.objects.filter(upload_path='default/user')[0]


class KvantUser(AbstractUser):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    permission = models.CharField(choices=permission, max_length=100)
    image = models.ForeignKey(ImageStorage, default=set_default_image, on_delete=models.SET(set_default_image))
    theme = models.CharField(max_length=100, choices=theme, default='light')
    color = models.CharField(max_length=100, choices=color, default='blue')

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
