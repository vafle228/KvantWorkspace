from django import forms

from LoginApp.models import KvantUser
from .models import *
from RegisterApp.services import getUserPersonalInfo


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
    class Meta:
        model = StudentParent
        exclude = ['document', 'adress']


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
    class Meta:
        model = StaffPersonalInfo
        exclude = ['user', 'document', 'study', 'adress']
