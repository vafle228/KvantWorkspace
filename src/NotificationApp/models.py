from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from NotificationApp.notifications.course_task import *
from NotificationApp.notifications.course_work import *
from NotificationApp.notifications.inotification import *
from NotificationApp.notifications.mail_receive import *
from NotificationApp.notifications.project_application import *
from NotificationApp.notifications.project_task import *


class KvantNotification(models.Model):
    notification    = GenericForeignKey('object_type', 'object_id')
    
    object_id       = models.PositiveIntegerField()
    object_type     = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    class Meta:
        db_table = 'kvant_notifications'
