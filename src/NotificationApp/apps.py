from django.apps import AppConfig
from django.db.models.signals import post_delete


class NotificationAppConfig(AppConfig):
    name = 'NotificationApp'

    def ready(self):
        from NotificationApp.models import KvantNotification

        for model in self.get_models():
            signal_func = self._wrapperCleaner
            
            if model == KvantNotification: 
                signal_func = self._notificationCleaner
            post_delete.connect(signal_func, sender=model, dispatch_uid=f'{model}')
        
        return super().ready()
    
    def _wrapperCleaner(self, sender, instance, **kwargs):
        from NotificationApp.services import getNotificationByGeneric
        
        notification = getNotificationByGeneric(instance)
        if notification.exists(): notification.first().delete()
    
    def _notificationCleaner(self, sender, instance, **kwargs):
        if instance.notification is not None: instance.notification.delete()
