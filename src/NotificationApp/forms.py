from django import forms
from .models import KvantNotification, MailNotification, TaskNotification


class NotificationSaveForm(forms.ModelForm):
    class Meta:
        model = KvantNotification
        fields = '__all__'


class MailNotificationSaveForm(forms.ModelForm):
    class Meta:
        model = MailNotification
        fields = '__all__'


class TaskNotificationSaveForm(forms.ModelForm):
    class Meta:
        model = TaskNotification
        fields = '__all__'