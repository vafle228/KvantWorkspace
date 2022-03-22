from django.db import models


class ChatMessage(models.Model):
    message = models.TextField()
    sender  = models.ForeignKey(to='LoginApp.KvantUser', on_delete=models.CASCADE)

    class Meta:
        db_table = 'message_chat'
    
    def __str__(self):
        return f'Сообщение {self.sender}'
