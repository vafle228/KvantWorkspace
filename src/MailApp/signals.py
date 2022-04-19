from .models import KvantMessage
from django.dispatch import receiver
from django.db.models.signals import pre_delete


@receiver(pre_delete, sender=KvantMessage)
def cleanMailM2MObjects(sender, instance, **kwargs):
    for file in instance.files.all(): file.delete()
    for receiver in instance.receivers.all(): receiver.delete()
