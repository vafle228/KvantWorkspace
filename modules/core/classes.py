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