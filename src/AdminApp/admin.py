from django.contrib import admin

from .forms import KvantCourseTypeSaveForm
from .models import KvantCourse, KvantCourseShedule, KvantCourseType


class KvantCourseTypeAdmin(admin.ModelAdmin):
    form = KvantCourseTypeSaveForm


admin.site.register(KvantCourse)
admin.site.register(KvantCourseShedule)
admin.site.register(KvantCourseType, KvantCourseTypeAdmin)
