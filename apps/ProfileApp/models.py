from django.db import models
from LoginApp.models import KvantUser


def get_path(instance, filename):
    return f'portfolio/{instance.user.username}/{filename}'


class KvantAward(models.Model):
    image = models.ImageField(upload_to=get_path)
    user = models.ForeignKey(KvantUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'Грамота: {self.user.__str__()}'
