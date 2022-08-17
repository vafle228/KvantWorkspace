from CoreApp.services.access import KvantTeacherAndAdminAccessMixin
from django.http import HttpResponse, JsonResponse
from django.views import generic
from LoginApp.services import getUserById
from RegisterApp.forms import TempRegisterLinkSaveForm

from AdminApp.forms import (CourseSheduleSaveForm, KvantCourseSaveForm,
                            KvantCourseTypeSaveForm)
from AdminApp.models import KvantCourseType,  KvantCourse

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


class SubjectDetailView(services.KvantCourseTypeAccessMixin, generic.DetailView):
    model               = KvantCourseType
    pk_url_kwarg        = 'subject_identifier'
    context_object_name = 'subject'
    template_name       = 'AdminApp/SubjectView/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(services.getSubjectData(ctx.get('subject')))

        return ctx


class SubjectsCreateView(services.KvantAdminAccessMixin, generic.View):
    def post(self, request, *args, **kwargs):
        object_manager = services.CourseSubjectManipulationManager([KvantCourseTypeSaveForm])
        return object_manager.createObject(request)


class SubjectUpdateView(services.KvantAdminAccessMixin, services.KvantCourseTypeAccessMixin, generic.View):
    def post(self, request, *args, **kwargs):
        subject = services.getSubjectById(kwargs.get('subject_identifier'))
        object_manager = services.CourseSubjectManipulationManager(
            [KvantCourseTypeSaveForm], object=subject)
        return object_manager.updateObject(request)


class CourseDetailView(services.KvantCourseAccessMixin, generic.DetailView):
    model               = KvantCourse
    pk_url_kwarg        = 'course_identifier'
    context_object_name = 'course'
    template_name       = 'AdminApp/CourseView/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(services.getCourseData(ctx.get('course')))

        return ctx


class CourseUpdateView(services.KvantAdminAccessMixin, services.KvantCourseAccessMixin, generic.View):
    def post(self, request, *args, **kwargs):
        course = services.getCourseById(kwargs.get('course_identifier'))
        object_manager = services.CourseManipulationManager(
            [KvantCourseSaveForm, CourseSheduleSaveForm], object=course)
        return object_manager.updateObject(request)


class CourseCreateView(services.KvantAdminAccessMixin, generic.View):
    def post(self, request, *args, **kwargs):
        object_manager = services.CourseManipulationManager(
            [KvantCourseSaveForm, CourseSheduleSaveForm])
        return object_manager.createObject(request)


class CourseLessonGenerateView(services.KvantAdminAccessMixin, services.KvantCourseAccessMixin, generic.View):
    def post(self, request, *args, **kwargs):
        services.GenerateCourseLessons(
            services.getCourseById(kwargs.get('course_identifier'))).generateLessons(
            request.POST.get('start_date'), request.POST.get('end_date'))
        return JsonResponse({'status': 200, 'link': 'Reload'})


class CourseLessonsDeleteView(services.KvantAdminAccessMixin, services.KvantCourseAccessMixin, generic.View):
    def dispatch(self, request, *args, **kwargs):
        kwargs.update(course_identifier=request.POST.get('course_identifier'))
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        services.deleteCourseLessons(
            services.getCourseById(kwargs.get('course_identifier')))
        return JsonResponse({'status': 200})


class ExcelImportDataView(KvantTeacherAndAdminAccessMixin, generic.View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(
            services.PersonalInfoExcelImport().importPersonalInfo(
                request.GET.get('user'), request.GET.getlist('users[]')),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


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


class CourseDeleteView(services.KvantCourseAccessMixin, services.KvantAdminAccessMixin, generic.View):
    def dispatch(self, request, *args, **kwargs):
        kwargs.update(course_identifier=request.POST.get('course_identifier'))
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        services.getCourseById(kwargs.get('course_identifier')).delete()
        return JsonResponse({'status': 200})


class SubjectsDeleteView(services.KvantCourseTypeAccessMixin, services.KvantAdminAccessMixin, generic.View):
    def dispatch(self, request, *args, **kwargs):
        kwargs.update(subject_identifier=request.POST.get('subject_identifier'))
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        services.getCourseTypeById(kwargs.get('subject_identifier')).delete()
        return JsonResponse({'status': 200})


class SubjectGroupView(KvantTeacherAndAdminAccessMixin, generic.TemplateView):
    template_name = 'AdminApp/GroupsView/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(groups=services.getSubjectGroups(self.request.GET.get('subject_identifier')))
        return ctx