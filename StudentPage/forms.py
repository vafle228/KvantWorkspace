from django import forms
from .models import FileStorage


class FileStorageSaveForm(forms.Form):
    file = forms.FileField()

    def save(self):
        file = self.cleaned_data['file']
        obj = FileStorage.objects.create(file)
        obj.save()

        return obj

