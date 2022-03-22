from django.db import models
from django.utils import timezone


class MailReceiver(models.Model):
    is_read  = models.BooleanField(default=False)
    receiver = models.ForeignKey(to='LoginApp.KvantUser', on_delete=models.CASCADE, related_name='receivers')

    class Meta:
        db_table = 'mail_receivers'

    def __str__(self):
        return f'Получатель {self.receiver}'


class KvantMessage(models.Model):
	# TODO: переделать DateField на DateTimeField + добавить спам фильтр
    text        = models.TextField(blank=True)
    receivers   = models.ManyToManyField(MailReceiver)
    date        = models.DateField(default=timezone.now)
    title       = models.CharField(max_length=120, default='Письмо')
    files       = models.ManyToManyField(to='CoreApp.FileStorage', blank=True)
    sender      = models.ForeignKey(to='LoginApp.KvantUser', on_delete=models.CASCADE, related_name='sender')

    class Meta:
        ordering = ['-date', '-id']
        db_table = 'kvant_messages'

    def __str__(self):
        receivers = list(map(str, [receiver for receiver in self.receivers.all()]))
        return f'Письмо от {self.sender} к {", ".join(receivers)}'


class ImportantMail(models.Model):
    mail = models.ForeignKey(KvantMessage, on_delete=models.CASCADE)
    user = models.ForeignKey(to='LoginApp.KvantUser', on_delete=models.CASCADE)

    class Meta:
        db_table = 'important_mails'

    def __str__(self):
        return f'Важное письмо {self.mail.sender}'
