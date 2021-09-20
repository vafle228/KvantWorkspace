from .models import KvantNews
from django.dispatch import receiver
from django.db.models.signals import pre_delete


@receiver(pre_delete, sender=KvantNews)
def clean_news_files(sender, instance, **kwargs):
    for file in instance.files.all():
        file.delete()
