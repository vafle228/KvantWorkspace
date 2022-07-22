from django.db import models
from django.urls import reverse_lazy as rl
from NotificationApp.notifications.inotification import INotification
from ProjectApp.models import MemberHiringKvantProject


class ProjectApplication(INotification):
    application = models.ForeignKey(to="ProjectApp.KvantProjectMembershipRequest", on_delete=models.CASCADE)

    @property
    def _project(self):
        return MemberHiringKvantProject.objects.get(requests__id=self.application.id).project.project

    @property
    def image_url(self):
        return self.application.sender.image.url
    
    @property
    def title(self):
        return self._project.title
    
    @property
    def description(self):
        user = f'{self.application.sender.surname} {self.application.sender.name}'
        if self.application.sender.patronymic is not None:
            user = f'{user} {self.application.sender.patronymic}'
        return f"<strong>{user}</strong> оставил заявку на участие"
    
    @property
    def redirect_link(self):
        return f"{rl('project_team', kwargs={'project_identifier': self._project.id})}"
