from django.contrib import admin
from .models import KvantAward
from .forms import KvantAwardSaveForm


class KvantAwardAdmin(admin.ModelAdmin):
    form = KvantAwardSaveForm


admin.site.register(KvantAward, KvantAwardAdmin)
