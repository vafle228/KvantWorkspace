from django.db import models


class INotification(models.Model):
    receiver = models.ForeignKey(to="LoginApp.KvantUser", on_delete=models.CASCADE)

    class Meta:
        abstract = True
        ordering = ['-id']
    
    @property
    def image_url(self):
        raise NotImplementedError
    
    @property
    def title(self):
        raise NotImplementedError
    
    @property
    def description(self):
        raise NotImplementedError
    
    @property
    def redirect_link(self):
        raise NotImplementedError