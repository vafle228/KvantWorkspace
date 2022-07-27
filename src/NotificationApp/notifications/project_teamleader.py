from django.db import models
from NotificationApp.notifications.inotification import INotification
from django.urls import reverse_lazy as rl


class TeamleaderChangeNotification(INotification):
    project     = models.ForeignKey(to="ProjectApp.KvantProject", on_delete=models.CASCADE)
    sender      = models.ForeignKey(to="LoginApp.KvantUser", related_name="changer", on_delete=models.CASCADE)
    manipulated = models.ForeignKey(to="LoginApp.KvantUser", related_name="changed", on_delete=models.CASCADE)
    
    @property
    def image_url(self):
        return self.sender.image.url
    
    @property
    def title(self):
        return self.project.title
    
    @property
    def description(self):
        user = f"{self.manipulated.surname} {self.manipulated.name}"
        if self.manipulated.patronymic is not None:
            user = f"{user} {self.manipulated.patronymic}"
        
        if self.receiver == self.manipulated:
            return f"<strong>Вы</strong> стали лидером команды проекта <strong>{self.project.title}</strong>"
        return f"<strong>{user}</strong> стал лидером команды"
    
    @property
    def redirect_link(self):
        return f'{rl("project_info", kwargs={"project_identifier": self.project.id})}'