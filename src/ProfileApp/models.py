from django.db import models


def get_path(instance, filename):
    return f'portfolio/{instance.user.username}/{filename}'


class KvantAward(models.Model):
    image = models.FileField(upload_to=get_path)
    user = models.ForeignKey(to='LoginApp.KvantUser', on_delete=models.CASCADE)

    class Meta:
        db_table = 'kvant_awards'

    def __str__(self):
        return f'Грамота: {self.user.__str__()}'