from django.contrib import admin
from .models import KvantAward, SocialInfo
from .forms import KvantAwardSaveForm, SocialInfoCreateForm


class KvantAwardAdmin(admin.ModelAdmin):
    form = KvantAwardSaveForm


class SocialInfoAdmin(admin.ModelAdmin):
    form = SocialInfoCreateForm


admin.site.register(SocialInfo, SocialInfoAdmin)
admin.site.register(KvantAward, KvantAwardAdmin)