from django import forms
from .models import KvantAward
from LoginApp.models import KvantUser
from core.mixins import ImageMixinBase, FileManagerMixinBase


class AwardMixin(ImageMixinBase, FileManagerMixinBase):    
    def clean_image(self):
        if self.instance.pk is None:
            return super().clean_image()
        
        to_path = f'portfolio/{self.cleaned_data.get("user").username}'
        from_path = "/".join(self.get_instance_image().name.split('/')[:-1])
        
        return self.change_directory(super().clean_image(), from_path, to_path)
    
    def get_image_file(self):
        return self.cleaned_data.get('image')
    
    def get_instance_image(self):
        return self.instance.image
    
    def is_file_moveable(self, file):
        is_file_changed = self.instance.image != file
        is_directory_changed = self.cleaned_data.get('user').username != self.instance.user.username
        
        return is_directory_changed and not is_file_changed

class KvantAwardSaveForm(forms.ModelForm, AwardMixin):
    class Meta:
        model = KvantAward
        fields = ['user', 'image']
    
    def __init__(self, *args, **kwargs):
        super(KvantAwardSaveForm, self).__init__(*args, **kwargs)
        super(AwardMixin, self).__init__(coef=0.65)