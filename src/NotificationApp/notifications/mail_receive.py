from django.db import models
from django.urls import reverse_lazy as rl
from NotificationApp.notifications.inotification import INotification


class MailReceiveNotification(INotification):
    mail = models.ForeignKey(to="MailApp.KvantMessage", on_delete=models.CASCADE)

    class Meta:
        db_table = 'mail_notifications'

    @property
    def redirect_link(self):
        return f"{rl('mail_box')}?type=received&mail={self.mail.id}"

    @property
    def description(self):
        return f'Отправил Вам сообщение <strong>{self.mail.title}</strong>'

    @property
    def image_url(self):
        return self.mail.sender.image.url
    
    @property
    def title(self):
        return f'{self.mail.sender.surname} {self.mail.sender.name}'
