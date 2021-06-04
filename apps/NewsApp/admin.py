from .models import KvantNews
from django.contrib import admin
from .forms import KvantNewsSaveForm


class KvantNewsAdmin(admin.ModelAdmin):
    form = KvantNewsSaveForm


admin.site.register(KvantNews, KvantNewsAdmin)
