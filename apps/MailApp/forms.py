from django import forms
from django.http import QueryDict
from LoginApp.models import KvantUser
from django.forms.utils import ErrorDict
from .models import KvantMessage, MailReceiver
from django.core.exceptions import ValidationError
from django.utils.datastructures import MultiValueDict


class MailReceiverSaveForm(forms.ModelForm):
    class Meta:
        model   = MailReceiver
        fields  = ('receiver', 'is_read')


class KvantMailSaveForm(forms.ModelForm):    
    class Meta:
        model   = KvantMessage
        fields  = ('sender', 'text', 'files', 'title')
    
    def __init__(self, *args, **kwargs):
        super(KvantMailSaveForm, self).__init__(*args, **kwargs)
        
        self.fields['title'].error_messages.update({
            'invalid': u'Заголовок невалиден.',
            'required': u'Заголовок не может быть пустым.',
            'max_length': u'Заголовок не может превышать %(max)d (сейчас %(length)d).',
        })


class KvantMailFillReceiversForm(forms.ModelForm):
    class Meta:
        model   = KvantMessage
        fields  = ('receivers', )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['receivers'].error_messages.update({
            'invalid_choice': u'Выбранный пользователь не существует.',
            'required': u'Письмо должно содержать хотябы одного получателя.',
        })
    
    def validate_users(self, input_users):
        receivers_user = []
        for user in input_users:
            if not KvantUser.objects.filter(id=user).exists():
                raise ValidationError(self.fields['receivers'].error_messages['invalid_choice'])
        
        for user in input_users:
            form = MailReceiverSaveForm({'receiver': KvantUser.objects.get(id=user)})
            receivers_user.append(str(form.save().id)) if form.is_valid() else None
        return receivers_user
    
    def full_clean(self):
        try:
            temp_dict = self.data.copy()
            receivers_users = self.validate_users(temp_dict.getlist('receivers'))
            
            temp_dict = temp_dict.dict()
            temp_dict['receivers'] = receivers_users

            new_args = QueryDict('', mutable=True)
            new_args.update(MultiValueDict(temp_dict))
            
            self.data = new_args
            return super().full_clean()
        
        except ValidationError as e:
            super().full_clean()
            self._errors = ErrorDict()
            self.add_error('receivers', e)

