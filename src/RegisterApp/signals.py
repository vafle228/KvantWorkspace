from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import *


@receiver(post_save, sender=StaffPersonalInfo)
def createStaffInfo(sender, instance, created, **kwards):
    if created:
        instance.adress = LivingAdress.objects.create()
        instance.document = PersonalityDocument.objects.create()
        instance.study = StudyDocument.objects.create()
        instance.scans = StaffDocumentFiles.objects.create()
        instance.save()


@receiver(post_save, sender=StudentPersonalInfo)
def createStudentInfo(sender, instance, created, **kwards):
    if created:
        instance.adress = LivingAdress.objects.create()
        instance.document = PersonalityDocument.objects.create()
        instance.mother = StudentParent.objects.create()
        instance.father = StudentParent.objects.create()
        instance.scans = StudentDocumentFiles.objects.create()
        instance.save()


@receiver(post_save, sender=StudentParent)
def createParentInfo(sender, instance, created, **kwards):
    if created:
        instance.adress = LivingAdress.objects.create()
        instance.document = PersonalityDocument.objects.create()
        instance.save()


@receiver(post_delete, sender=StaffPersonalInfo)
def cleanStaffO2OObjects(sender, instance, **kwargs):
    instance.study.delete()
    instance.document.delete()
    instance.adress.delete()
    instance.scans.delete()


@receiver(post_delete, sender=StudentPersonalInfo)
def cleanStudentO2OObjects(sender, instance, **kwargs):
    instance.mother.delete()
    instance.father.delete()
    instance.document.delete()
    instance.adress.delete()
    instance.scans.delete() 

@receiver(post_delete, sender=StudentParent)
def cleanParentO2OObjects(sender, instance, **kwargs):
    instance.document.delete()
    instance.adress.delete()
