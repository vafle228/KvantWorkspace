from django.db import models
from DiaryApp.models import KvantLesson


class KvantNotification(models.Model):
    redirect_link   = models.TextField()
    image_url       = models.TextField()
    title           = models.CharField(max_length=255)
    description     = models.CharField(max_length=255)
    object_name     = models.CharField(max_length=255)
    receiver        = models.ForeignKey(to='LoginApp.KvantUser', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']
        db_table = 'kvant_notifications'

    def __str__(self):
        return f'Уведомление {self.title}'


class MailNotification(models.Model):
    redirect_link   = models.TextField()
    receiver        = models.ForeignKey(to='LoginApp.KvantUser', on_delete=models.CASCADE)
    mail_obj        = models.ForeignKey(to='MailApp.KvantMessage', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']
        db_table = 'mail_notifications'

    @property
    def description(self):
        return 'Отправил Вам сообщение'

    @property
    def image_url(self):
        return self.mail_obj.sender.image.url
    
    @property
    def title(self):
        return f'{self.mail_obj.sender.surname} {self.mail_obj.sender.name}'
    
    @property
    def object_name(self):
        return self.mail_obj.title


class TaskNotification(models.Model):
    redirect_link   = models.TextField()
    receiver        = models.ForeignKey(to='LoginApp.KvantUser', on_delete=models.CASCADE)
    task_obj        = models.ForeignKey(to='DiaryApp.KvantHomeTask', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']
        db_table = 'task_notifications'
    
    @property
    def _course(self):
        return KvantLesson.objects.get(tasks__id=self.task_obj.id).course

    @property
    def description(self):
        if self.receiver.permission == 'Учитель':
            return 'Появилось новая работа по теме'
        return 'Появилось новое задание по теме'

    @property
    def image_url(self):
        return self._course.type.image.url
    
    @property
    def title(self):
        return f'{self._course}'
    
    @property
    def object_name(self):
        return self.task_obj.base.title