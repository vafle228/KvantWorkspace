from django.views import generic

from AdminApp.forms import (CourseSheduleSaveForm, KvantCourseSaveForm,
                            KvantCourseTypeSaveForm)
from CoreApp.services.access import KvantTeacherAndAdminAccessMixin

from . import services


class AdminsTableTemplateView(KvantTeacherAndAdminAccessMixin, generic.TemplateView):
    template_name = "AdminApp/AdminsTable/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(admins=services.allUsers('Администратор'))

        return context


class TeachersTableTemplateView(KvantTeacherAndAdminAccessMixin, generic.TemplateView):
    template_name = "AdminApp/TeachersTable/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(teachers=services.allUsers('Учитель'))

        return context


class StudentsTableTemplateView(KvantTeacherAndAdminAccessMixin, generic.TemplateView):
    template_name = "AdminApp/StudentsTable/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(students=services.allUsers('Ученик'))

        return context


class CoursesTableTemplateView(KvantTeacherAndAdminAccessMixin, generic.TemplateView):
    template_name = "AdminApp/CoursesTable/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'courses': services.allCourses(),
            'subjects': services.allSubjects(),
            'teachers': services.allUsers('Учитель'),
            'students': services.allUsers('Ученик'),
        })

        return context


class SubjectsTableTemplateView(KvantTeacherAndAdminAccessMixin, generic.TemplateView):
    template_name = "AdminApp/SubjectsTable/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(subjects=services.allSubjects())

        return context


class SubjectsCreateView(KvantTeacherAndAdminAccessMixin, generic.View):
    def post(self, request, *args, **kwargs):
        object_manager = services.CourseSubjectManipulationManager([KvantCourseTypeSaveForm])
        return object_manager.createObject(request)


class CourseCreateView(KvantTeacherAndAdminAccessMixin, generic.View):
    def post(self, request, *args, **kwargs):
        object_manager = services.CourseManipulationManager(
            [KvantCourseSaveForm, CourseSheduleSaveForm])
        return object_manager.createCourse(request)
