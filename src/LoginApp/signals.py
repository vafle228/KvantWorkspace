from django.db.models.signals import post_save
from django.dispatch import receiver
from ProfileApp.models import SocialInfo
from RegisterApp.models import StaffPersonalInfo, StudentPersonalInfo

from .models import KvantUser


@receiver(post_save, sender=KvantUser)
def cleanNewsFiles(sender, instance, created, **kwards):
    if created: SocialInfo.objects.create(user=instance)
    if created and instance.permission != 'Ученик': StaffPersonalInfo.objects.create(user=instance)
    if created and instance.permission == 'Ученик': StudentPersonalInfo.objects.create(user=instance)
