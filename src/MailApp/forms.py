from CoreApp.services.m2m import FileM2MBaseMixin, ManyToManyObjectCreateMixin
from CoreApp.services.utils import buildDate
from django import forms
from django.core.exceptions import ValidationError
from LoginApp.services import getUserById, isUserExists

from .models import KvantMessage, MailReceiver


class MailReceiverSaveForm(forms.ModelForm):
    class Meta:
        model = MailReceiver
        fields = ('receiver', 'is_read')


class KvantMailSaveForm(forms.ModelForm):
    class Meta:
        model = KvantMessage
        fields = ('sender', 'text', 'title')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].error_messages.update({
            'invalid': u'Заголовок невалиден.',
            'required': u'Заголовок не может быть пустым.',
            'max_length': u'Заголовок не может превышать %(limit_value)d (сейчас %(show_value)d).',
        })
    
    def clean_title(self):
        if not self.cleaned_data.get('title').isprintable():
            raise forms.ValidationError('Заголовок содержит невалидые символы')
        if '/' in self.cleaned_data.get('title'):
            raise forms.ValidationError('Заголовок не может содержать символ "/".')
        return self.cleaned_data.get('title')


class KvantMailFileSaveForm(FileM2MBaseMixin):
    class Meta:
        model = KvantMessage
        fields = ('files',)

    def __init__(self, *args, **kwargs):
        super().__init__('files', *args, **kwargs)

        self.fields['files'].error_messages.update({
            'max_upload_count': u'Объект не может содеражть более 16 файлов',
            'max_upload_weight': u'Суммарный объем файлов не может превышать 32mB.',
        })
    
    def getFileUploadPath(self):
        return f'mail/{buildDate(self.instance.date)}/{self.instance.title}'


class KvantMailReceiversForm(ManyToManyObjectCreateMixin):
    class Meta:
        model = KvantMessage
        fields = ('receivers',)

    def __init__(self, *args, **kwargs):
        super().__init__('receivers', *args, **kwargs)

        self.fields['receivers'].error_messages.update({
            'invalid_choice': u'Выбранный пользователь не существует.',
            'required': u'Письмо должно содержать хотя бы одного получателя.',
        })
    
    def getData(self):
        return self.data.getlist('receivers')
    
    def validateValue(self, values):
        if not values:
            raise ValidationError(self.fields['receivers'].error_messages['required'])
        if not self._validateUsers(values):
            raise ValidationError(self.fields['receivers'].error_messages['invalid_choice'])

    def createObjects(self, values):
        receivers_user = []
        for user in values:
            form = MailReceiverSaveForm({'receiver': getUserById(user)})
            if form.is_valid(): receivers_user.append(str(form.save().id)) 
        return receivers_user

    def _validateUsers(self, users):
        """ Валидация пользователей на существование """
        for user in users:
            if not isUserExists(user): return False
        return True
