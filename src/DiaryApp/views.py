from . import services
from django.views import generic
from DiaryApp.models import KvantLesson, KvantHomeTask
from .forms import HomeWorkFilesSaveForm, HomeWorkSaveForm
from CoreApp.services.utils import getMonthName


class DiaryPageListView(services.DiaryMonthValidateMixin, generic.ListView):
    model               = KvantLesson
    ordering            = ['-date', '-id']
    template_name       = 'DiaryApp/DiaryPage/index.html'
    context_object_name = 'lessons'

    def dispatch(self, request, *args, **kwargs):
        kwargs.update({
            'month_num': request.GET.get('period'),})
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return services.getDiaryLessonQuery(
            self.request.user, self.request.GET.get('period'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        period = self.request.GET.get('period')
        context.update({
            'month': getMonthName(period),
            'next': services.DiaryPaginator().generateNext(int(period)),
            'prev': services.DiaryPaginator().generatePrev(int(period)),
        })
        return context


class LessonDetailView(services.LessonAccessMixin, generic.DetailView):
    model               = KvantLesson
    pk_url_kwarg        = 'lesson_identifier'
    context_object_name = 'lesson'
    template_name       = 'DiaryApp/LessonDetailView/index.html'


class TaskDetailView(services.TaskAccessMixin, generic.DetailView):
    model               = KvantHomeTask
    pk_url_kwarg        = 'task_identifier'
    context_object_name = 'task'
    template_name       = 'DiaryApp/TaskDetailView/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'work': services.getUserWork(kwargs.get('object'), self.request.user),})
        return context


class HomeWorkCreateView(services.TaskAccessMixin, generic.View):
    def dispatch(self, request, *args, **kwargs):
        kwargs.update({
            'task_identifier': self.request.POST.get('task_id'),})
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        object_manager = services.HomeWorkManipulationManager(
            [HomeWorkSaveForm, HomeWorkFilesSaveForm])
        return object_manager.createTaskWork(request)


class HomeWorkUpdateView(services.WorkEditAccessMixin, generic.View):
    def post(self, request, *args, **kwargs):
        work = services.getWorkById(self.kwargs.get('work_identifier'))
        object_manager = services.HomeWorkManipulationManager(
            [HomeWorkSaveForm, HomeWorkFilesSaveForm], object=work
        )
        return object_manager.updateObject(request)
    