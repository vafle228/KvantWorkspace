from django.views import generic

from . import services


class AdminsTableTemplateView(generic.TemplateView):
    template_name = "AdminApp/AdminsTable/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(admins=services.allUsers('Администратор'))

        return context


class TeachersTableTemplateView(generic.TemplateView):
    template_name = "AdminApp/TeachersTable/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(teachers=services.allUsers('Учитель'))

        return context


class StudentsTableTemplateView(generic.TemplateView):
    template_name = "AdminApp/StudentsTable/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(students=services.allUsers('Ученик'))

        return context


class CoursesTableTemplateView(generic.TemplateView):
    template_name = "AdminApp/CoursesTable/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(courses=services.allCourses())

        return context


class SubjectsTableTemplateView(generic.TemplateView):
    template_name = "AdminApp/SubjectsTable/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(subjects=services.allSubjects())

        return context