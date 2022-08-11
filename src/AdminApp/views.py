from CoreApp.services.access import KvantTeacherAndAdminAccessMixin
from django.http import HttpResponse, JsonResponse
from django.views import generic
from LoginApp.services import getUserById
from RegisterApp.forms import TempRegisterLinkSaveForm

from AdminApp.forms import (CourseSheduleSaveForm, KvantCourseSaveForm,
                            KvantCourseTypeSaveForm)
from AdminApp.models import KvantCourseType

from . import services


class AdminsTableTemplateView(KvantTeacherAndAdminAccessMixin, generic.TemplateView):
    template_name = "AdminApp/AdminsTable/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(admins=services.allUsers('Администратор'))

        services.PersonalInfoExcelImport().importPersonalInfo('Ученик')

        return context


class TeachersTableTemplateView(KvantTeacherAndAdminAccessMixin, generic.TemplateView):
    template_name = "AdminApp/TeachersTable/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            teachers=services.allUsers('Учитель'),
            subjects=KvantCourseType.objects.all(),
        )

        return context


class StudentsTableTemplateView(KvantTeacherAndAdminAccessMixin, generic.TemplateView):
    template_name = "AdminApp/StudentsTable/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            students=services.allUsers('Ученик'),
            subjects=KvantCourseType.objects.all(),
        )

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


class SubjectsCreateView(services.KvantAdminAccessMixin, generic.View):
    def post(self, request, *args, **kwargs):
        object_manager = services.CourseSubjectManipulationManager([KvantCourseTypeSaveForm])
        return object_manager.createObject(request)


class CourseCreateView(services.KvantAdminAccessMixin, generic.View):
    def post(self, request, *args, **kwargs):
        object_manager = services.CourseManipulationManager(
            [KvantCourseSaveForm, CourseSheduleSaveForm])
        return object_manager.createCourse(request)


class ExcelImportDataView(KvantTeacherAndAdminAccessMixin, generic.View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(
            services.PersonalInfoExcelImport().importPersonalInfo(request.GET.get('user')),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )


class GenerateUserCreateLink(services.KvantAdminAccessMixin, generic.View):
    def dispatch(self, request, *args, **kwargs):
        request.POST = request.GET; return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        manager = services.GenerateRegisterLink([TempRegisterLinkSaveForm])
        response = HttpResponse(manager.createRegisterLink(request), content_type="text/plain; charset=utf-8")
        response['Content-Disposition'] = 'attachment; filename="links.txt";'
        
        return response


class UserDeleteView(services.KvantUserDeleteAccessMixin, generic.View):
    def dispatch(self, request, *args, **kwargs):
        kwargs.update(user_identifier=request.POST.get('user_identifier'))
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        getUserById(kwargs.get('user_identifier')).delete()
        return JsonResponse({'status': 200})


class CourseDeleteView(services.KvantCourseDeleteAccessMixin, generic.View):
    def dispatch(self, request, *args, **kwargs):
        kwargs.update(course_identifier=request.POST.get('course_identifier'))
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        services.getCourseById(kwargs.get('course_identifier')).delete()
        return JsonResponse({'status': 200})


class SubjectsDeleteView(services.KvantCourseTypeDeleteAccessMixin, generic.View):
    def dispatch(self, request, *args, **kwargs):
        kwargs.update(subject_identifier=request.POST.get('subject_identifier'))
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        services.getCourseTypeById(kwargs.get('subject_identifier')).delete()
        return JsonResponse({'status': 200})
