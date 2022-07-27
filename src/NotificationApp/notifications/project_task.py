from django.db import models
from NotificationApp.notifications.inotification import INotification
from django.urls import reverse_lazy as rl

from ProjectApp.models import KvantProject


class ProjectTask(INotification):
    task = models.ForeignKey(to="ProjectApp.KvantProjectTask", on_delete=models.CASCADE)
    
    class Meta:
        abstract = True
    
    @property
    def _project(self):
        return KvantProject.objects.get(tasks__id=self.task.id)
    
    @property
    def image_url(self):
        return self.sender.image.url
    
    @property
    def title(self):
        return self._project.title


class ProjectTaskCreate(ProjectTask):
    sender  = models.ForeignKey(to="LoginApp.KvantUser", related_name="add_invoker", on_delete=models.CASCADE)

    @property
    def description(self):
        user = f'{self.sender.surname} {self.sender.name}'
        if self.sender.patronymic is not None:
            user = f'{user} {self.sender.patronymic}'
        return f'<strong>{user}</strong> добавил новое задание <strong>{self.task.title}</strong>'

    @property
    def redirect_link(self):
        rl_args = {
            "task_identifier": self.task.id,
            "project_identifier": self._project.id,
        }
        return f'{rl("task_view", kwargs=rl_args)}'


class ProjectTaskUpdate(ProjectTask):
    sender  = models.ForeignKey(to="LoginApp.KvantUser", related_name="upd_invoker", on_delete=models.CASCADE)

    @property
    def description(self):
        user = f'{self.sender.surname} {self.sender.name}'
        if self.sender.patronymic is not None:
            user = f'{user} {self.sender.patronymic}'
        return f'<strong>{user}</strong> изменил задание <strong>{self.task.title}</strong>'

    @property
    def redirect_link(self):
        rl_args = {
            "task_identifier": self.task.id,
            "project_identifier": self._project.id,
        }
        return f'{rl("task_view", kwargs=rl_args)}'
