from AdminApp.models import KvantCourseType
from django.views import generic

from .services import services, access
from .forms import (KvantProjectFilesSaveForm, KvantProjectTypeSaveForm,
                    KvantProjectParticipantsSaveForm, KvantProjectSaveForm)
from .models import KvantProject, KvantProjectTask
from CoreApp.services.access import KvantWorkspaceAccessMixin


class ProjectCatalogTemplateView(KvantWorkspaceAccessMixin, generic.ListView):
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


class ProjectInfoDetailView(access.KvantProjectExistsMixin, generic.DetailView):
    model               = KvantProject
    pk_url_kwarg        = 'project_identifier'
    context_object_name = 'project'
    template_name       = 'ProjectApp/ProjectInfo/index.html'


class ProjectWorkspaceDetailView(access.ProjectWorkspaceAccessMixin, generic.DetailView):
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


class ProjectTaskDetailView(access.ProjectTaskAccessMixin, generic.DetailView):
    model               = KvantProjectTask
    pk_url_kwarg        = 'task_identifier'
    context_object_name = 'task'
    template_name       = 'ProjectApp/ProjectTaskView/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            project=services.getProjectByTaskId(kwargs.get('object').id),
        )
        return context


class ProjectStatusUpdateView(access.ProjectTaskChangeStatusMixin, generic.View):
    def dispatch(self, request, *args, **kwargs):
        kwargs.update({
            'task_identifier': request.POST.get('task_identifier')
        })
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        task = services.getTaskById(kwargs.get('task_identifier'))
        object_manager = services.TaskObjectManipulationManager(
            [KvantProjectTypeSaveForm], object=task)
        return object_manager.updateObject(request)


class ProjectTaskUpdateView(access.ProjectTaskUpdateMixin, generic.View):
    def post(self, request, *args, **kwargs):
        task = services.getTaskById(kwargs.get('task_identifier'))
        object_manager = services.TaskObjectManipulationManager(
            [KvantProjectSaveForm, KvantProjectParticipantsSaveForm, KvantProjectFilesSaveForm], object=task)
        return object_manager.updateObject(request)


class ProjectTaskCreateView(access.ProjectTaskCreateMixin, generic.View):
    def dispatch(self, request, *args, **kwargs):
        kwargs.update({
            'project_identifier': request.POST.get('project_identifier')
        })
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        project = services.getProjectById(kwargs.get('project_identifier'))
        object_manager = services.TaskObjectManipulationManager(
            [KvantProjectSaveForm, KvantProjectParticipantsSaveForm, KvantProjectFilesSaveForm])
        return object_manager.createTaskProject(request, project)
