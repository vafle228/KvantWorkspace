from django import forms
from LoginApp.models import KvantUser
from .models import KvantMessage, MailReceiver


class MailReceiverSaveForm(forms.ModelForm):
    class Meta:
        model = MailReceiver
        fields = ['receiver', 'is_read']


class KvantMailSaveForm(forms.ModelForm):    
    class Meta:
        model = KvantMessage
        fields = ['sender', 'text', 'files', 'title']
    
    def __init__(self, *args, **kwargs):
        super(KvantMailSaveForm, self).__init__(*args, **kwargs)
        
        self.fields['title'].error_messages.update({
            'invalid': u'Заголовок невалиден.',
            'required': u'Заголовок не может быть пустым.',
            'max_length': u'Заголовок не может превышать %(max)d (сейчас %(length)d).',
        })

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
