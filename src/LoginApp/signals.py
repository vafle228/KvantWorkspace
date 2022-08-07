from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import KvantUser
from ProfileApp.models import SocialInfo


@receiver(post_save, sender=KvantUser)
def cleanNewsFiles(sender, instance, created, **kwards):
    if created: SocialInfo.objects.create(user=instance)