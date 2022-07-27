from django.db import models
from NotificationApp.notifications.inotification import INotification
from django.urls import reverse_lazy as rl


class TeamManipulation(INotification):
    project = models.ForeignKey(to="ProjectApp.KvantProject", on_delete=models.CASCADE)

    @property
    def title(self):
        return self.project.title
    
    @property
    def redirect_link(self):
        return f'{rl("project_info", kwargs={"project_identifier": self.project.id})}'



class TeamApplyNotification(TeamManipulation):
    sender      = models.ForeignKey(to="LoginApp.KvantUser", related_name="applier", on_delete=models.CASCADE)
    manipulated = models.ForeignKey(to="LoginApp.KvantUser", related_name="applied", on_delete=models.CASCADE)

    @property
    def image_url(self):
        return self.sender.image.url
    
    @property
    def description(self):
        user = f"{self.manipulated.surname} {self.manipulated.name}"
        if self.manipulated.patronymic is not None:
            user = f"{user} {self.manipulated.patronymic}"
        
        if self.receiver == self.manipulated:
            return f"Вас приняли в команду проекта <strong>{self.project.title}</strong>"
        return f"<strong>{user}</strong> принят в команду проекта"


class TeamKickNotification(TeamManipulation):
    sender      = models.ForeignKey(to="LoginApp.KvantUser", related_name="kicker", on_delete=models.CASCADE)
    manipulated = models.ForeignKey(to="LoginApp.KvantUser", related_name="kicked", on_delete=models.CASCADE)

    @property
    def image_url(self):
        return self.sender.image.url
    
    @property
    def description(self):
        user = f"{self.manipulated.surname} {self.manipulated.name}"
        if self.manipulated.patronymic is not None:
            user = f"{user} {self.manipulated.patronymic}"
        
        if self.receiver == self.manipulated:
            return f"Вас исключили из проекта <strong>{self.project.title}</strong>"
        return f"<strong>{user}</strong> исключен из команды проекта"
    

    
