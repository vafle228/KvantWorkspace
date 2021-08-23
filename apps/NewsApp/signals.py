from .models import KvantNews
from django.dispatch import receiver
from SystemModule.forms import FileStorageSaveForm
from django.db.models.signals import pre_delete, pre_save


@receiver(pre_delete, sender=KvantNews)
def clean_news_files(sender, instance, **kwargs):
    for file in instance.files.all():
        file.delete()
