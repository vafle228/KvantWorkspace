from django.dispatch import receiver
from .models import KvantNews, setDefaultImage
from django.db.models.signals import pre_delete


@receiver(pre_delete, sender=KvantNews)
def clean_news_files(sender, instance, **kwargs):
    if setDefaultImage() != instance.image:
        instance.image.delete()
    [file.delete() for file in instance.files.all()]
