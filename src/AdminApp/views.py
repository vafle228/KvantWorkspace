from django.views import generic
from LoginApp.models import KvantUser
from .models import KvantCourse, KvantCourseType


class AdminsTableTemplateView(generic.TemplateView):
    template_name = "AdminApp/AdminsTable/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(admins=KvantUser.objects.filter(permission='Администратор'))

        return context


class TeachersTableTemplateView(generic.TemplateView):
    template_name = "AdminApp/TeachersTable/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(teachers=KvantUser.objects.filter(permission='Учитель'))

        return context


class StudentsTableTemplateView(generic.TemplateView):
    template_name = "AdminApp/StudentsTable/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(students=KvantUser.objects.filter(permission='Ученик'))

        return context


class CoursesTableTemplateView(generic.TemplateView):
    template_name = "AdminApp/CoursesTable/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(courses=KvantCourse.objects.all())

        return context


class SubjectsTableTemplateView(generic.TemplateView):
    template_name = "AdminApp/SubjectsTable/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(subjects=KvantCourseType.objects.all())

        return context