from AdminApp.services import getCourseById, getCourseQuery
from CoreApp.services.access import KvantTeacherAndAdminAccessMixin
from CoreApp.services.objects import CreateOrUpdateObject
from JournalApp.forms import KvantBaseFilesSaveForm, KvantBaseSaveForm
from DiaryApp.models import KvantTaskBase
from JournalApp.services import access, queryget, utils
from django.views import generic


class JournalPageTemplateView(KvantTeacherAndAdminAccessMixin, generic.TemplateView):
    """ Контроллер общей страницы журнала """
    template_name = 'JournalApp/JournalPage/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'courses': getCourseQuery(self.request.user),})
        return context


class JournalDetailView(access.KvantJournalAccessMixin, generic.TemplateView):
    """ Контроллер получения конкретного журнала """
    template_name = 'JournalApp/JournalView/index.html'

    def dispatch(self, request, *args, **kwargs):
        kwargs.update({
            'period': self.request.GET.get('period'),
            'course_identifier': self.request.GET.get('course_id'),})
        return super(access.KvantJournalAccessMixin, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'lessons': queryget.getJournalLessonQuery(
                getCourseById(self.request.GET.get('course_id')), self.request.GET.get('period')),
            'students': getCourseById(self.request.GET.get('course_id')).students,})
        return context


class CheckingPageDetailView(access.KvantBaseAccessMixin, generic.DetailView):
    """ Контроллер страницы оценивания """
    model               = KvantTaskBase
    pk_url_kwarg        = 'base_identifier'
    context_object_name = 'base'
    template_name       = 'JournalApp/CheckingPage/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'type': queryget.getBaseType(kwargs.get('object')),
            'students': queryget.getBaseStudents(kwargs.get('object')),
            'first_stat': utils.KvantBaseStatistic(kwargs.get('object')).countWorkComplete(),
            'second_stat': utils.KvantBaseStatistic(kwargs.get('object')).countWorkQuality(),})
        return context


class UpdateBaseView(access.KvantBaseAccessMixin, generic.View):
    """ Контроллер обновления заданий """
    def post(self, request, *args, **kwargs):
        base = queryget.getBaseById(kwargs.get('base_identifier'))
        object_creator = CreateOrUpdateObject(
            [KvantBaseSaveForm, KvantBaseFilesSaveForm], object=base)
        base_or_errors = object_creator.updateObject(request)
        return utils.KvantBaseManupulationResponse().getResponse(base_or_errors)


class CreateTaskView(access.KvantLessonAccessMixin, generic.View):
    """ Контроллер создания заданий """
    def dispatch(self, request, *args, **kwargs):
        kwargs.update({
            'lesson_identifier': self.request.POST.get('lesson_id'),})
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        lesson = queryget.getLessonById(kwargs.get('lesson_identifier'))
        object_creator = utils.KvantTaskCreator(
            [KvantBaseSaveForm, KvantBaseFilesSaveForm])
        base_or_errors = object_creator.createKvantTask(request, lesson)
        return utils.KvantBaseManupulationResponse().getResponse(base_or_errors)


class UpdateMarksView(access.KvantBaseAccessMixin, generic.View):
    """ Контроллер обновления отметок """
    def post(self, request, *args, **kwargs):
        mark_creator = utils.KvantBaseMarksUpdate(request)
        base = queryget.getBaseById(self.kwargs.get('base_identifier'))
        
        return mark_creator.createKvantMarks(base)
