from django import template

from NotificationApp.models import KvantNotification


register = template.Library()


def getUserNotifications(user):
    return [
        wrapper for wrapper in KvantNotification.objects.all() 
        if wrapper.notification.receiver == user
    ]


register.filter('user_notifications', getUserNotifications)
