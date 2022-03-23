from AdminApp.models import KvantCourseType
from django.views import generic

from . import services
from .forms import (KvantProjectFilesSaveForm,
                    KvantProjectParticipantsSaveForm, KvantProjectSaveForm)
from .models import KvantProject, KvantProjectTask


class ProjectCatalogTemplateView(generic.ListView):
    model               = KvantProject
    ordering            = ['-date', '-id']
    paginate_by         = 10
    template_name       = 'ProjectApp/ProjectCatalog/index.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return services.KvantProjectQuerySelector(self.request).getCatalogQuery()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(subjects=KvantCourseType.objects.all())
        return context


class ProjectInfoDetailView(generic.DetailView):
    model               = KvantProject
    pk_url_kwarg        = 'project_identifier'
    context_object_name = 'project'
    template_name       = 'ProjectApp/ProjectInfo/index.html'


class ProjectWorkspaceDetailView(generic.DetailView):
    model               = KvantProject
    pk_url_kwarg        = 'project_identifier'
    context_object_name = 'project'
    template_name       = 'ProjectApp/ProjectWorkspace/index.html'

    def get_object(self, queryset=None):
        return services.getActiveProject(super().get_object(queryset))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(services.updateTaskContext(kwargs.get('object').project))
        return context


class ProjectTaskDetailView(generic.DetailView):
    model               = KvantProjectTask
    pk_url_kwarg        = 'task_identifier'
    context_object_name = 'task'
    template_name       = 'ProjectApp/ProjectTaskView/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(services.getProjectTeam(kwargs.get('object')))
        return context


class ProjectTaskUpdateView(generic.View):
    def post(self, request, *args, **kwargs):
        task = services.getTaskById(kwargs.get('task_identifier'))
        object_manager = services.TaskObjectManipulationManager(
            [KvantProjectSaveForm, KvantProjectParticipantsSaveForm, KvantProjectFilesSaveForm], object=task)
        return object_manager.updateObject(request)


class ProjectTaskCreateView(generic.View):
    def post(self, request, *args, **kwargs):
        project = services.getProjectById(kwargs.get('project_identifier'))
        object_manager = services.TaskObjectManipulationManager(
            [KvantProjectSaveForm, KvantProjectParticipantsSaveForm, KvantProjectFilesSaveForm])
        return object_manager.createTaskProject(request, project)
