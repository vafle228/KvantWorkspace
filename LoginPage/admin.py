from . import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import KvantUserCreationForm, KvantUserChangeForm


class KvantUserAdmin(UserAdmin):
    add_form = KvantUserCreationForm
    form = KvantUserChangeForm
    model = models.KvantUser
    list_display = ('username', 'email', 'surname', 'name', 'patronymic', 'permission')
    list_filter = ('username', 'email', 'surname', 'name', 'patronymic', 'permission')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'surname', 'name', 'patronymic', 'permission')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'surname', 'name', 'patronymic', 'permission', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(models.KvantAdmin)
admin.site.register(models.KvantTeacher)
admin.site.register(models.KvantStudent)
admin.site.register(models.KvantUser, KvantUserAdmin)
