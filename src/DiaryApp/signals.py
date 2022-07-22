from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver

from .models import KvantHomeTask, KvantHomeWork, KvantLesson, KvantTaskBase


@receiver(pre_delete, sender=KvantTaskBase)
def cleanBaseM2MObjects(sender, instance, **kwargs):
    for mark in instance.marks.all(): mark.delete()
    for file in instance.files.all(): file.delete()


@receiver(pre_delete, sender=KvantLesson)
def cleanLessonM2MObjects(sender, instance, **kwargs):
    for task in instance.tasks.all(): task.base.delete()


@receiver(post_delete, sender=KvantLesson)
def cleanLessonO2OObject(sender, instance, **kwargs):
    instance.base.delete()


@receiver(pre_delete, sender=KvantHomeTask)
def cleanTaskM2MObjects(sender, instance, **kwargs):
    for work in instance.works.all(): work.delete()


@receiver(post_delete, sender=KvantHomeTask)
def cleanTaskO2OObject(sender, instance, **kwargs):
    instance.base.delete()


@receiver(pre_delete, sender=KvantHomeWork)
def cleanWorkM2MObjects(sender, instance, **kwargs):
    for file in instance.files.all(): file.delete()
