from DiaryApp.models import KvantLesson
from django.db import models
from django.urls import reverse_lazy as rl
from NotificationApp.notifications.inotification import INotification


class TaskNotification(INotification):
    task = models.ForeignKey(to='DiaryApp.KvantHomeTask', on_delete=models.CASCADE)
    
    class Meta:
        abstract = True
    
    @property
    def _lesson(self):
        return KvantLesson.objects.get(tasks__id=self.task.id)
    
    @property
    def _course(self): return self._lesson.course
    
    @property
    def redirect_link(self):
        lesson = self._lesson
        return f"{rl('diary_page')}?period={lesson.date.month}&lesson={lesson.base.id}"

    @property
    def image_url(self):
        return self._course.type.image.url
    
    @property
    def title(self): return f'{self._course}'


class TaskCreateNotification(TaskNotification):
    class Meta:
        db_table = 'taskcreate_notifications'

    @property
    def description(self):
        return f'Появилось новое задание <strong>{self.task.base.title}</strong>'


class TaskUpdateNotification(TaskNotification):
    class Meta:
        db_table = 'taskupdate_notifications'

    @property
    def description(self):
        return f'Задание <strong>{self.task.base.title}</strong> изменено'
