from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *


@receiver(post_save, sender=StaffPersonalInfo)
def createStaffInfo(sender, instance, created, **kwards):
    if created:
        instance.adress = LivingAdress.objects.create()
        instance.document = PersonalityDocument.objects.create()
        instance.study = StudyDocument.objects.create()
        instance.save()


@receiver(post_save, sender=StudentPersonalInfo)
def createStudentInfo(sender, instance, created, **kwards):
    if created:
        instance.adress = LivingAdress.objects.create()
        instance.document = PersonalityDocument.objects.create()
        instance.mother = StudentParent.objects.create()
        instance.father = StudentParent.objects.create()
        instance.save()


@receiver(post_save, sender=StudentParent)
def createParentInfo(sender, instance, created, **kwards):
    if created:
        instance.adress = LivingAdress.objects.create()
        instance.document = PersonalityDocument.objects.create()
        instance.save()
