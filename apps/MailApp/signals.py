from .models import KvantMessage
from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save


@receiver(pre_delete, sender=KvantMessage)
def clean_mail_files(sender, instance, **kwargs):
    [file.delete() for file in instance.files.all()]
