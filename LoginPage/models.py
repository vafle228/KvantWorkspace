from django.db import models
from django.contrib.auth.models import AbstractUser


permission = (("Ученик", "Ученик"),
              ("Учитель", "Учитель"),
              ("Администратор", "Администратор")
              )


class KvantUser(AbstractUser):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    permission = models.CharField(choices=permission, max_length=100)

    def __str__(self):
        return f'{self.permission} {self.surname} {self.name[0]}.{self.patronymic[0]}.'
