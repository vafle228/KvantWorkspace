from django.contrib import admin
from .models import ImageStorage, FileStorage


admin.site.register(ImageStorage)
admin.site.register(FileStorage)
