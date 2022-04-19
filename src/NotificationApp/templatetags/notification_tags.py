from django import template
from NotificationApp.models import TaskNotification, MailNotification


register = template.Library()


def getUserNotifications(user):
    return list(TaskNotification.objects.filter(receiver=user)) + list(MailNotification.objects.filter(receiver=user))


register.filter('user_notifications', getUserNotifications)
