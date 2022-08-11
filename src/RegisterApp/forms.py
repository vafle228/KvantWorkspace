import secrets

from django import forms
from LoginApp.forms import KvantUserCreationForm
from LoginApp.models import KvantUser

from RegisterApp.services import getUserPersonalInfo

from .models import *


class PersonalityDocumentSaveForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = PersonalityDocument


class LivingAdressSaveForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = LivingAdress


class StudyDocumentSaveForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = StudyDocument


class StudentParentSaveForm(forms.ModelForm):
    additional_forms = [
        (LivingAdressSaveForm, lambda u: u.adress),
        (PersonalityDocumentSaveForm, lambda u: u.document),
    ]

    class Meta:
        model = StudentParent
        exclude = ['document', 'adress']
    

    def is_valid(self):
        for form, inst in self.additional_forms:
            form = form(self.data, instance=inst(self.instance))
            if not form.is_valid():
                self._errors = form._errors; return False
        return super().is_valid()     
    
    def save(self, commit=True):
        for form, inst in self.additional_forms:
            form = form(self.data, instance=inst(self.instance))
            form.save() if form.is_valid() else None
        return super().save(commit)


class UserInfoSaveForm(forms.ModelForm):
    class Meta:
        model = KvantUser
        fields = ['surname', 'name', 'email', 'patronymic']


class UserInfoSaveMixin(forms.ModelForm):
    additional_forms = [
        (UserInfoSaveForm, lambda u: u),
        (LivingAdressSaveForm, lambda u: getUserPersonalInfo(u).adress),
        (PersonalityDocumentSaveForm, lambda u: getUserPersonalInfo(u).document),
    ]
    
    def is_valid(self):
        for form, inst in self.additional_forms:
            form = form(self.data, instance=inst(self.instance.user))
            if not form.is_valid():
                self._errors = form._errors; return False
        return super().is_valid()     
    
    def save(self, commit=True):
        for form, inst in self.additional_forms:
            form = form(self.data, instance=inst(self.instance.user))
            form.save() if form.is_valid() else None
        return super().save(commit)


class StudentPersonalInfoSaveForm(UserInfoSaveMixin):
    class Meta:
        model = StudentPersonalInfo
        exclude = ['user', 'mother', 'father', 'adress', 'document']


class StaffPersonalInfoSaveForm(UserInfoSaveMixin):
    additional_forms = [
        (UserInfoSaveForm, lambda u: u),
        (StudyDocumentSaveForm, lambda u: getUserPersonalInfo(u).study),
        (LivingAdressSaveForm, lambda u: getUserPersonalInfo(u).adress),
        (PersonalityDocumentSaveForm, lambda u: getUserPersonalInfo(u).document),
    ]

    class Meta:
        model = StaffPersonalInfo
        exclude = ['user', 'document', 'study', 'adress']


class TempRegisterLinkSaveForm(forms.ModelForm):
    count = forms.IntegerField(min_value=0)
    
    class Meta:
        fields = ['permission']
        model = TempRegisterLink
    
    def save(self, commit=True):
        links = list()
        for _ in range(self.cleaned_data.get('count')):
            hex_val = secrets.token_hex(16)
            while TempRegisterLink.objects.filter(key=hex_val).exists():
                hex_val = secrets.token_hex(16)
            
            links.append(TempRegisterLink.objects.create(
                key=hex_val, permission=self.cleaned_data.get('permission')))
        return links


class UserRegisterForm(KvantUserCreationForm):
    password2 = forms.CharField(max_length=255)

    def clean_password2(self):
        if self.cleaned_data.get('password2') is None:
            raise ValidationError('Подтвердите пароль')
        if self.cleaned_data.get('password2') != self.cleaned_data.get('password'):
            raise ValidationError('Пароли должны совпадать')
        return super().clean_password2()
