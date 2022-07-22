from DiaryApp.models import KvantHomeTask, KvantLesson
from django.db import models
from django.urls import reverse_lazy as rl
from NotificationApp.notifications.inotification import INotification


class WorkNotification(INotification):
    work = models.ForeignKey(to="DiaryApp.KvantHomeWork", on_delete=models.CASCADE)

    class Meta:
        abstract = True

    @property
    def _task(self):
        return KvantHomeTask.objects.get(works__id=self.work.id)
    
    @property
    def _lesson(self):
        return KvantLesson.objects.get(tasks__works__id=self.work.id)
    
    @property
    def _course(self): return self._lesson.course
    
    @property
    def redirect_link(self):
        return f"{rl('checking_page', kwargs={'base_identifier': self._task.base.id})}"

    @property
    def image_url(self):
        return self.work.sender.image.url
    
    @property
    def title(self): return f'{self._course}'


class WorkCreateNotification(WorkNotification):
    class Meta:
        db_table = 'workcreate_notifications'

    @property
    def description(self):
        return f'<strong>{self.work.sender}</strong> добавил работу по заданию <strong>{self._task.base.title}</strong>'


class WorkUpdateNotification(WorkNotification):
    class Meta:
        db_table = 'workupdate_notifications'
    
    @property
    def description(self):
        return f'<strong>{self.work.sender}</strong> изменил работу по заданию <strong>{self._task.base.title}</strong>'
