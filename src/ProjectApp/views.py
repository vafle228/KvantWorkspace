from AdminApp.models import KvantCourseType
from AdminApp.services import allUsers
from CoreApp.services.access import (KvantTeacherAndAdminAccessMixin,
                                     KvantWorkspaceAccessMixin)
from django.http import HttpResponse
from django.views import generic
from LoginApp.services import getUserById

from .forms import (KvantApplicationSaveForm, KvantProjectFilesSaveForm,
                    KvantProjectLeadersSaveForm, KvantProjectSaveForm,
                    KvantProjectSubjectSaveForm, KvantProjectTaskFilesSaveForm,
                    KvantProjectTaskParticipantsSaveForm,
                    KvantProjectTaskSaveForm, KvantProjectTypeSaveForm)
from .models import KvantProject, KvantProjectTask
from .services import access, services


class ProjectCatalogTemplateView(KvantWorkspaceAccessMixin, generic.ListView):
    model               = KvantProject
    ordering            = ['-date', '-id']
    paginate_by         = 10
    template_name       = 'ProjectApp/ProjectCatalog/index.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return services.KvantProjectQuerySelector(
            self.request.user, self.request.GET
        ).getCatalogQuery()
    
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
        context.update(project=services.getProjectById(self.kwargs.get('project_identifier')))
        
        return context


class ProjectStatusUpdateView(access.ProjectTaskManipulationMixin, generic.View):
    def dispatch(self, request, *args, **kwargs):
        kwargs.update({
            'task_identifier': request.POST.get('task_identifier')})
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        task = services.getTaskById(kwargs.get('task_identifier'))
        project = services.getProjectById(kwargs.get('project_identifier'))
        object_manager = services.TaskManipulationManager(
            [KvantProjectTypeSaveForm], object=task)
        return object_manager.updateTaskProject(request, project)


class ProjectTaskUpdateView(access.ProjectTaskManipulationMixin, generic.View):
    def post(self, request, *args, **kwargs):
        task = services.getTaskById(kwargs.get('task_identifier'))
        project = services.getProjectById(kwargs.get('project_identifier'))
        object_manager = services.TaskManipulationManager(
            [KvantProjectTaskSaveForm, KvantProjectTaskParticipantsSaveForm, KvantProjectTaskFilesSaveForm], object=task)
        return object_manager.updateTaskProject(request, project)


class ProjectTaskDeleteView(access.ProjectTaskManipulationMixin, generic.View):
    def post(self, request, *args, **kwargs):
        services.getTaskById(kwargs.get('task_identifier')).delete()
        return HttpResponse('Ok')


class ProjectTaskCreateView(access.ProjectTaskManipulationMixin, generic.View):
    def post(self, request, *args, **kwargs):
        project = services.getProjectById(kwargs.get('project_identifier'))
        object_manager = services.TaskManipulationManager(
            [KvantProjectTaskSaveForm, KvantProjectTaskParticipantsSaveForm, KvantProjectTaskFilesSaveForm])
        return object_manager.createTaskProject(request, project)
    
    def _taskExiststTest(self, object_id): return True


class ProjectApplicationSaveView(access.ProjectApplicationCreateMixin, generic.View):
    def post(self, request, *args, **kwargs):
        project = services.getClassedProject(
            services.getProjectById(kwargs.get('project_identifier')))
        object_manager = services.ApplicationManipulationManager([KvantApplicationSaveForm])
        return object_manager.createProjectApplication(request, project.memberhiringkvantproject)


class MemberRequestManipulationView(access.ProjectApplicationManageMixin, generic.View):
    def dispatch(self, request, *args, **kwargs):
        kwargs.update(application_identifier=request.POST.get('application_identifier'))
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        services.ProjectTeamManager(
            services.getProjectById(kwargs.get('project_identifier'))).projectMemeberJoin(
            services.getRequestById(request.POST.get('application_identifier')),  request)
        return HttpResponse('Ok')


class ChangeProjectTeamleaderView(access.KvantProjectManageMixin, generic.View):
    def post(self, request, *args, **kwargs):
        services.ProjectTeamManager(
            services.getProjectById(kwargs.get('project_identifier'))
        ).changeTeamleader(request)
        return HttpResponse('Ok')


class HiringManipulationView(access.KvantProjectManageMixin, generic.View):
    def post(self, request, *args, **kwargs):
        services.ProjectStatusManager(services.getClassedProject(
            services.getProjectById(kwargs.get('project_identifier'))
        )).hiringStatusManager(request.POST.get('choise'))
        return HttpResponse('Ok')


class KickMemberView(access.KvantProjectManageMixin, generic.View):
    def post(self, request, *args, **kwargs):
        services.ProjectTeamManager(
            services.getProjectById(kwargs.get('project_identifier'))
        ).projectMemberKick(request)
        return HttpResponse('OK')


class ProjectFinishView(access.KvantProjectManageMixin, generic.View):
    def post(self, request, *args, **kwargs):
        services.ProjectStatusManager(services.getClassedProject(
            services.getProjectById(kwargs.get('project_identifier'))
        )).closeProjectManager()
        return HttpResponse('OK')


class ProjectCreateView(KvantTeacherAndAdminAccessMixin, generic.View):
    def post(self, request, *args, **kwargs):
        object_manager = services.ProjectManipulationManager(
            [KvantProjectLeadersSaveForm, KvantProjectSaveForm, 
            KvantProjectSubjectSaveForm, KvantProjectFilesSaveForm])
        return object_manager.createProject(request)


class ProjectUpdateView(access.KvantProjectManageMixin, generic.View):
    def post(self, request, *args, **kwargs):
        project = services.getProjectById(kwargs.get('project_identifier'))
        object_manager = services.ProjectManipulationManager(
            [KvantProjectSaveForm, KvantProjectFilesSaveForm], object=project)
        return object_manager.updateObject(request)
