from abc import abstractmethod

from CoreApp.forms import FileStorageSaveForm
from CoreApp.models import FileStorage
from django import forms
from django.forms import ValidationError
from django.forms.utils import ErrorDict

from .utils import getSizeWithSuffix


class ManyToManyObjectCreateMixin(forms.ModelForm):
    """ Дополнение класса ModelForm для создания m2m объектов """
    def __init__(self, field, *args, **kwargs):
        self.field_name = field
        super().__init__(*args, **kwargs)

    @abstractmethod
    def validateValue(self, values):
        """ Метод для валидации входных данных """
        raise NotImplementedError
    
    @abstractmethod
    def createObjects(self, values):
        """ Метод для создания m2m объектов """
        raise NotImplementedError
    
    @abstractmethod
    def getData(self):
        """ Метод для получения данных для работы """
        raise NotImplementedError
    
    def clean(self):
        """ Изменение логики clean метода, для адаптации под m2m """
        try:
            self._errors = ErrorDict()
            self.validateValue(self.getData())
        except ValidationError as e:
            self.add_error(self.field_name, e)
            return super().clean()
        else:
            self.cleaned_data.update({
                self.field_name: self.createObjects(self.getData())
            })
            return super().clean()


class FileM2MBaseMixin(ManyToManyObjectCreateMixin):
    def __init__(self, field, *args, **kwargs):
        super().__init__(field, *args, **kwargs)
        
        self.max_count = kwargs.get('max_count') or 16
        self.max_weight = kwargs.get('max_weight') or 32 * 1024 * 1024
        self.fields[field].error_messages.update({
            'max_upload_count': f'Объект не может содеражть более {self.max_count} файлов',
            'max_upload_weight': f'Суммарный объем файлов не может превышать {getSizeWithSuffix(self.max_weight)}.',
        })
    
    def getData(self):
        if not self.cleaned_data.get(self.field_name):
            return self.files.getlist(self.field_name)
        return self.files.getlist(self.field_name) + list(self.cleaned_data[self.field_name])
    
    def validateValue(self, values):
        if len(values) > self.max_count: 
            raise ValidationError(self.fields[self.field_name].error_messages['max_upload_count'])
        if not self._validateFileSumSize(values):
            raise ValidationError(self.fields[self.field_name].error_messages['max_upload_weight'])
    
    def createObjects(self, values):
        instance_files = []
        for file in values:
            form = self._createFileStorageInstance(file, self.getFileUploadPath())
            if form.is_valid(): instance_files.append(form.save().id)
        return instance_files
    
    @abstractmethod
    def getFileUploadPath(self):
        """ Путь для сохранения файлов. Определяется индивидуально """
        raise NotImplementedError
    
    def _createFileStorageInstance(self, file, path):
        """ 
        Инициализация формы создания файлов FileStorage.
        Если сущность уже FileStorage, то форма обновления.
        """
        if isinstance(file, FileStorage):
            return FileStorageSaveForm({'upload_path': path}, instance=file)
        return FileStorageSaveForm({'upload_path': path}, {'file': file})
    
    def _normalizeData(self, values):
        """ 
        Стандартизация данных для дальнейшего удобства. 
        FileStorage instance приводятся в InMemoryUploaded сущности
        """
        return [file.file if isinstance(file, FileStorage) else file for file in values]

    def _validateFileSumSize(self, values):
        """ Валидация суммарного веса всех файлов """
        size_count = 0
        for file in self._normalizeData(values):
            size_count += file.size
            if size_count > self.max_weight: return False
        return size_count < self.max_weight
