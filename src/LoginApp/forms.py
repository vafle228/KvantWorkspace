from django import forms
from .models import KvantUser
from CoreApp.services.image import ImageThumbnailBaseMixin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import SetPasswordForm


class UserImageManagerMixin(ImageThumbnailBaseMixin):
    def clean_image(self):
        if self.instance.image == self.cleaned_data.get('image'):
            return self.instance.image
        return self.makeImageThumbnail(self.cleaned_data.get('image'))  


class KvantUserCreationForm(UserCreationForm, UserImageManagerMixin):
    def __init__(self, *args, **kwargs):
        super(KvantUserCreationForm, self).__init__(*args, **kwargs)
        super(UserImageManagerMixin, self).__init__(coef=0.3)
    
    class Meta:
        model = KvantUser
        fields = ('username', 'email', 'name', 'surname', 'patronymic', 'permission', 'image')


class KvantUserChangeForm(UserChangeForm, UserImageManagerMixin):
    def __init__(self, *args, **kwargs):
        super(KvantUserChangeForm, self).__init__(*args, **kwargs)
        super(UserImageManagerMixin, self).__init__(coef=0.3)
    
    class Meta:
        model = KvantUser
        fields = ('username', 'email', 'password', 'name', 'surname', 'patronymic', 'image')


class ImageChangeForm(forms.ModelForm, UserImageManagerMixin):
        def __init__(self, *args, **kwargs):
            super(ImageChangeForm, self).__init__(*args, **kwargs)
            super(UserImageManagerMixin, self).__init__(coef=0.3)
        
        class Meta:
            model = KvantUser
            fields = ('image', )


class PasswordChangeForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.get('instance'); super().__init__(user, *args, **{})
