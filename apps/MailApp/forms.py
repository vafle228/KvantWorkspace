from django import forms
from LoginApp.models import KvantUser
from .models import KvantMessage, MailReceiver
from django.core.exceptions import ValidationError
from SystemModule.forms import FileStorageSaveForm
from core.mixins import ManyToManyObjectCreateMixin


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


class KvantMailFileSaveForm(ManyToManyObjectCreateMixin):
    class Meta:
        model = KvantMessage
        fields = ('files',)

    def __init__(self, *args, **kwargs):
        super().__init__('files', *args, **kwargs)

        self.fields['files'].error_messages.update({
            'max_upload_count': u'Объект не может содеражть более 16 файлов',
            'max_upload_weight': u'Суммарный объем файлов не может превышать 32mB.',
        })
    
    def get_data(self):
        return self.files.getlist('files')

    def validate_value(self, values):
        if len(values) > 16:
            raise ValidationError(self.fields['files'].error_messages['max_upload_count'])
        size_count = 0
        for file in values:
            size_count += file.size

            if size_count > 32 * 1024 * 1024:
                raise ValidationError(self.fields['files'].error_messages['max_upload_weight'])

    def create_objects(self, values):
        mail_files = []
        mail = self.instance
        for file in values:
            form = FileStorageSaveForm(
                {'upload_path': f'mail/{mail.date}/{mail.title}'}, {'file': file}
            )
            mail_files.append(str(form.save().id)) if form.is_valid() else None
        return mail_files


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
    
    def get_data(self):
        return self.data.getlist('receivers')
    
    def validate_value(self, values):
        if not values:
            raise ValidationError(self.fields['receivers'].error_messages['required'])
        
        for user in values:
            if not KvantUser.objects.filter(id=user).exists():
                raise ValidationError(self.fields['receivers'].error_messages['invalid_choice'])

    def create_objects(self, values):
        receivers_user = []
        for user in values:
            form = MailReceiverSaveForm({
                'receiver': KvantUser.objects.get(id=user)
            })
            receivers_user.append(str(form.save().id)) if form.is_valid() else None
        return receivers_user     
