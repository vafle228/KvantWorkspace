from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from CoreApp.services.access import KvantObjectExistsMixin
from django.contrib.contenttypes.models import ContentType

from .models import KvantNotification


class NotificationBaseManger:
    def broadcastNotification(self, **kwargs):
        channel_layer = get_channel_layer()
        wrapper = self._wrapNotification(self.buildBase(**kwargs))

        if wrapper is not None and wrapper.notification.receiver.is_active:

            async_to_sync(channel_layer.group_send)(
                f'notification_{wrapper.notification.receiver.id}',
                {
                    'type': 'user_notification',

                    'id': wrapper.id,
                    'title': wrapper.notification.title,
                    'image_url': wrapper.notification.image_url,
                    'description': wrapper.notification.description,
                    'redirect_link': wrapper.notification.redirect_link,
                },
            )
    
    def _wrapNotification(self, notification):
        return KvantNotification.objects.create(
            object_id=notification.id, object_type=ContentType.objects.get_for_model(type(notification)),
        )
    
    def buildBase(self, **kwargs): raise NotImplementedError


def getNotificationById(id):
    return KvantNotification.objects.get(id=id)


def deleteNotification(id):
    return getNotificationById(id).delete()


def getNotificationByGeneric(generic):
    return KvantNotification.objects.filter(
        object_id=generic.id, object_type=ContentType.objects.get_for_model(generic)
    )


class NotificationAccessMixin(KvantObjectExistsMixin):
    request_object_arg = 'notification_identifier'

    def accessTest(self, **kwargs):
        if super().accessTest(**kwargs):
            wrapper = getNotificationById(kwargs.get('notification_identifier'))
            return self._notificationAccessTest(wrapper, kwargs.get('user'))
        return False
    
    def _notificationAccessTest(self, wrapper, user):
        return wrapper.notification.receiver == user
    
    def _objectExiststTest(self, object_id):
        return KvantNotification.objects.filter(id=object_id).exists()
