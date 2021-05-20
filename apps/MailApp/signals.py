from .models import KvantMessage
from django.dispatch import receiver
from django.db.models.signals import pre_delete


@receiver(pre_delete, sender=KvantMessage)
def clean_mail_files(sender, instance, **kwargs):
    [file.delete() for file in instance.files.all()]
    [receiver_user.delete() for receiver_user in instance.receivers.all()]
