from django import forms
from LoginApp.models import KvantUser
from .models import KvantMessage, MailReceiver


class MailReceiverSaveForm(forms.ModelForm):
    class Meta:
        model = MailReceiver
        fields = ['receiver']


class KvantMailSaveForm(forms.ModelForm):
    class Meta:
        model = KvantMessage
        fields = ['sender', 'text', 'style_text', 'files', 'title']

    def save(self, request):
        return self.fill_mail_receivers(request, super(KvantMailSaveForm, self).save())
    
    def fill_mail_receivers(self, request, mail):
        for user_id in request.POST.getlist('receivers'):
            user_form = MailReceiverSaveForm(
                {'receiver': KvantUser.objects.get(id=user_id)}
            )
            if user_form.is_valid():
                mail.receivers.add(user_form.save())
        return mail
