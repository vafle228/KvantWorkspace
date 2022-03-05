from .models import KvantUser
from CoreApp.services.image import ImageThumbnailBaseMixin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class UserImageManagerMixin(ImageThumbnailBaseMixin):
    def clean_image(self):
        if self.instance.image == self.cleaned_data.get('image'):
            return self.instance.image
        return self.makeImageThumbnail(self.cleaned_data.get('image'))  


class KvantUserCreationForm(UserCreationForm, UserImageManagerMixin):
    def __init__(self, *args, **kwargs):
        super(KvantUserCreationForm, self).__init__(*args, **kwargs)
        super(UserImageManagerMixin, self).__init__(coef=0.2)
    
    class Meta:
        model = KvantUser
        fields = ('username', 'email', 'password', 'name', 'surname', 'patronymic', 'image')


class KvantUserChangeForm(UserChangeForm, UserImageManagerMixin):
    def __init__(self, *args, **kwargs):
        super(KvantUserChangeForm, self).__init__(*args, **kwargs)
        super(UserImageManagerMixin, self).__init__(coef=0.35)
    
    class Meta:
        model = KvantUser
        fields = ('username', 'email', 'password', 'name', 'surname', 'patronymic', 'image')
