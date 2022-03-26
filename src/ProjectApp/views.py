from AdminApp.models import KvantCourseType
from CoreApp.services.access import KvantWorkspaceAccessMixin
from django.http import HttpResponse
from django.views import generic
from LoginApp.models import KvantUser
from LoginApp.services import getUserById

from AdminApp.services import allUsers

from .forms import (KvantApplicationSaveForm, KvantProjectFilesSaveForm,
                    KvantProjectSaveForm, KvantProjectSubjectSaveForm,
                    KvantProjectTaskFilesSaveForm,
                    KvantProjectTaskParticipantsSaveForm,
                    KvantProjectTaskSaveForm, KvantProjectTypeSaveForm)
from .models import (ClosedKvantProject, KvantProject, KvantProjectTask,
                     MemberHiringKvantProject)
from .services import access, services


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
        context.update({
            'students': allUsers('Ученик'),
            'subjects': KvantCourseType.objects.all(),
        })
        return context


class ProjectInfoDetailView(access.KvantProjectExistsMixin, generic.DetailView):
    model               = KvantProject
    pk_url_kwarg        = 'project_identifier'
    context_object_name = 'project'
    template_name       = 'ProjectApp/ProjectInfo/index.html'

    def get_object(self, queryset=None):
        return services.getClassedProject(super().get_object(queryset))


class ProjectWorkspaceDetailView(access.ProjectWorkspaceAccessMixin, generic.DetailView):
    model               = KvantProject
    pk_url_kwarg        = 'project_identifier'
    context_object_name = 'project'
    template_name       = 'ProjectApp/ProjectWorkspace/index.html'

    def get_object(self, queryset=None):
        return services.getClassedProject(super().get_object(queryset))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(services.updateTaskContext(kwargs.get('object').project))
        
        return context


class ProjectTeamManagerDetailView(access.ProjectWorkspaceAccessMixin, generic.DetailView):
    model               = KvantProject
    pk_url_kwarg        = 'project_identifier'
    context_object_name = 'project'
    template_name       = 'ProjectApp/ProjectTeamManager/index.html'

    def get_object(self, queryset=None):
        return services.getClassedProject(super().get_object(queryset))


class ProjectTaskDetailView(access.ProjectTaskAccessMixin, generic.DetailView):
    model               = KvantProjectTask
    pk_url_kwarg        = 'task_identifier'
    context_object_name = 'task'
    template_name       = 'ProjectApp/ProjectTaskView/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(project=services.getProjectById(kwargs.get('project_identifier')))
        
        return context


class ProjectStatusUpdateView(access.ProjectTaskChangeStatusMixin, generic.View):
    def dispatch(self, request, *args, **kwargs):
        kwargs.update({
            'task_identifier': request.POST.get('task_identifier')})
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        task = services.getTaskById(kwargs.get('task_identifier'))
        object_manager = services.TaskManipulationManager(
            [KvantProjectTypeSaveForm], object=task)
        return object_manager.updateObject(request)


class ProjectTaskUpdateView(access.ProjectTaskUpdateMixin, generic.View):
    def post(self, request, *args, **kwargs):
        task = services.getTaskById(kwargs.get('task_identifier'))
        object_manager = services.TaskManipulationManager(
            [KvantProjectTaskSaveForm, KvantProjectTaskParticipantsSaveForm, KvantProjectTaskFilesSaveForm], object=task)
        return object_manager.updateObject(request)


class ProjectTaskCreateView(access.ProjectTaskCreateMixin, generic.View):
    def post(self, request, *args, **kwargs):
        project = services.getProjectById(kwargs.get('project_identifier'))
        object_manager = services.TaskManipulationManager(
            [KvantProjectTaskSaveForm, KvantProjectTaskParticipantsSaveForm, KvantProjectTaskFilesSaveForm])
        return object_manager.createTaskProject(request, project)


class ProjectApplicationSaveView(access.KvantProjectExistsMixin, generic.View):
    def post(self, request, *args, **kwargs):
        project = services.getClassedProject(
            services.getProjectById(kwargs.get('project_identifier')))
        object_manager = services.ApplicationManipulationManager(
            [KvantApplicationSaveForm], project.memberhiringkvantproject)
        return object_manager.createProjectApplication(request)


class MemberRequestManipulationView(generic.View):
    def post(self, request, *args, **kwargs):
        project = services.getProjectById(kwargs.get('project_identifier'))
        mem_request = services.getRequestById(request.POST.get('request_identifier'))

        if request.POST.get('choise') == 'accept':
            project.team.add(mem_request.sender)
        mem_request.delete()
        return HttpResponse('Ok')


class HiringManipulationView(generic.View):
    """ КОСТЫЛЬ! ПЕРЕДЕЛАЙ! """
    def post(self, request, *args, **kwargs):
        project = services.getClassedProject(
            services.getProjectById(kwargs.get('project_identifier')))

        if request.POST.get('choise') == 'on':
            MemberHiringKvantProject.objects.create(project=project)
        
        elif MemberHiringKvantProject.objects.filter(project__project=project.project).exists():
            MemberHiringKvantProject.objects.get(project__project=project.project).delete()
        return HttpResponse('Ok')


class KickMemberView(generic.View):
    """ КОСТЫЛЬ! ПЕРЕДЕЛАЙ! """
    def post(self, request, *args, **kwargs):
        project = services.getProjectById(kwargs.get('project_identifier'))
        user = getUserById(request.POST.get('user_identifier'))

        project.team.remove(user)

        return HttpResponse('OK')


class FinishProject(generic.View):
    """ КОСТЫЛЬ! ПЕРЕДЕЛАЙ! """
    def post(self, request, *args, **kwargs):
        project = services.getClassedProject(
            services.getProjectById(kwargs.get('project_identifier')))
        project_instance = project.project

        project.delete()
        ClosedKvantProject.objects.create(project=project_instance)

        return HttpResponse('OK')


class ProjectCreateView(generic.View):
    def post(self, request, *args, **kwargs):
        object_manager = services.ProjectManipulationManager(
            [KvantProjectSaveForm, KvantProjectSubjectSaveForm, KvantProjectFilesSaveForm])
        return object_manager.createProject(request)
