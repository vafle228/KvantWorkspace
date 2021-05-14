from django.db import models
from django.utils import timezone
from LoginApp.models import KvantUser
from SystemModule.models import FileStorage, ImageStorage


class KvantMessage(models.Model):
    text = models.TextField(blank=True)
    style_text = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now)
    files = models.ManyToManyField(FileStorage, blank=True)
    title = models.CharField(max_length=120, default='Письмо')
    sender = models.ForeignKey(KvantUser, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(KvantUser, on_delete=models.CASCADE, related_name='receiver')

    def __str__(self):
        return f'Письмо от {self.sender} к {self.receiver}'
