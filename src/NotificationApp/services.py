from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class NotificationBaseManger:
    def broadcastNotification(self, **kwargs):
        channel_layer = get_channel_layer()
        notification = self.buildNotification(**kwargs)

        if notification.receiver.is_active:

            async_to_sync(channel_layer.group_send)(
                f'notification_{notification.receiver.id}',
                {
                    'type': 'user_notification',
                    'title': notification.title,
                    'image_url': notification.image_url,
                    'description': notification.description,
                    'object_name': notification.object_name,
                    'redirect_link': notification.redirect_link,
                },
            )
    
    def buildNotification(self, **kwargs):
        raise NotImplementedError
