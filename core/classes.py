from django.views.generic import View
from LoginApp.models import KvantUser
from django.shortcuts import redirect


class KvantJournalAccessMixin(View):
    # Метод делегирования запроса
    def dispatch(self, request, *args, **kwargs):
        from django.urls import reverse_lazy
        
        user_id = kwargs['identifier']
        if not self.is_available(user_id):  # Проверка на доступ
            return redirect(reverse_lazy('login_page'))
        return super().dispatch(request, *args, **kwargs)  # Исполняем родительский метод

    def is_available(self, identifier):
        from django.contrib import messages

        if KvantUser.objects.filter(id=identifier).exists():  # Проверяем существование
            request_user = self.request.user  # Пользователь который запросил
            requested_user = KvantUser.objects.filter(id=identifier)[0]  # Пользовательн которого запросили
            if request_user == requested_user and requested_user.is_authenticated:  # Проверка совпадения
                return True

        # Ошибка в случаи не совпадения или отсутсвия
        messages.error(self.request, 'Отказано в доступе!')
        return False


class ModelsFileFiller:
    def __init__(self, root_directory, container):
        from SystemModule.forms import FileStorageSaveForm
        
        self.container = container
        self.form = FileStorageSaveForm
        self.root_directory = root_directory
    
    def fill_model_files(self, files_query, directory_name):
        from os.path import join
        from django.utils import timezone
        
        today = timezone.now().date()
        upload_path = join(self.root_directory, f'files/{today}/{directory_name}')
        for file in files_query:
            file_form = self.form(
                {'upload_path': upload_path}, {'file': file}
            )
            if file_form.is_valid():
                self.container.add(file_form.save())