from django.contrib import admin
from .models import FileStorage
from .forms import FileStorageSaveForm


class FileStorageAdmin(admin.ModelAdmin):
    form = FileStorageSaveForm

admin.site.register(FileStorage, FileStorageAdmin)
