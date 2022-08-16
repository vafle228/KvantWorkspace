from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver

from .models import (ActiveKvantProject, ClosedKvantProject, KvantProject,
                     KvantProjectTask, MemberHiringKvantProject)


@receiver(pre_delete, sender=MemberHiringKvantProject)
def cleanProjectApplications(sender, instance, **kwargs):
    for request in instance.requests.all(): request.delete()


@receiver(pre_delete, sender=ActiveKvantProject)
def cleanProjectChat(sender, instance, **kwargs):
    for msg in instance.chat.all(): msg.delete()


@receiver(pre_delete, sender=KvantProject)
def cleanProject(sender, instance, **kwargs):
    for file in instance.files.all(): file.delete()
    for task in instance.tasks.all(): task.delete()


@receiver(pre_delete, sender=KvantProjectTask)
def cleanProjectTasks(sender, instance, **kwargs):
    for file in instance.files.all(): file.delete()


@receiver(post_delete, sender=ClosedKvantProject)
def deleteProject(sender, instance, **kwargs):
    instance.project.delete()
