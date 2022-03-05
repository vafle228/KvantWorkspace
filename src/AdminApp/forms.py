from CoreApp.services.filemanager import FileMoveBaseMixin
from CoreApp.services.image import ImageThumbnailBaseMixin
from django import forms

from .models import KvantCourseType


class ImageManagerMixin(ImageThumbnailBaseMixin, FileMoveBaseMixin):
    def clean_image(self):
        if not self.errors:
            return self._updateImageValue()
        return self.cleaned_data.get('image')
        
    def _updateImageValue(self):
        if self.instance.image == self.cleaned_data.get('image'):
            return self.changeDirectory(
                self.instance.image, f'courses/{self.instance.name}'
            )
        return self.makeImageThumbnail(self.cleaned_data.get('image'))  
    

class KvantCourseTypeSaveForm(forms.ModelForm, ImageManagerMixin):
    class Meta:
        model = KvantCourseType
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(KvantCourseTypeSaveForm, self).__init__(*args, **kwargs)
        super(ImageManagerMixin, self).__init__(coef=0.25)
        
        self.fields['name'].error_messages.update({
            'invalid': u'Заголовок невалиден.',
            'required': u'Заголовок не может быть пустым.',
            'max_length': u'Заголовок не может превышать %(limit_value)d (сейчас %(show_value)d).',
        })
        self.fields['image'].error_messages.update({
            'invalid': u'Превью курса повреждено или не является изображением.'
        })

    def clean_name(self):
        if not self.cleaned_data.get('name').isprintable():
            raise forms.ValidationError('Название содержит невалидые символы.')
        if '/' in self.cleaned_data.get('name'):
            raise forms.ValidationError('Название не может содержать символ "/".')
        return self.cleaned_data.get('name')
