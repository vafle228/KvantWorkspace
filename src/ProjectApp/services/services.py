from CoreApp.services.utils import ObjectManipulationManager
from django.urls import reverse_lazy as rl
from ProjectApp.models import (ActiveKvantProject, ClosedKvantProject,
                               KvantProject, KvantProjectTask,
                               MemberHiringKvantProject, KvantProjectMembershipRequest)


class KvantProjectQuerySelector:
    def __init__(self, request):
        self.user = request.user
        self.search_param = request.GET.get('search')

        self.subject = request.GET.get('subject') or 'all'
        self.filter_type = request.GET.get('filter') or 'all'
        
    def getCatalogQuery(self):
        if self.search_param is None:
            return self._getProjectQuery()
        return self._getProjectQuery().filter(title__contains=self.search_param)
    
    def _getProjectQuery(self):
        project_data = {
            'all': lambda: KvantProject.objects.all(),
            
            'closed': lambda: KvantProject.objects.filter(
                id__in=ClosedKvantProject.objects.values_list('project__id', flat=True)),
            
            'active': lambda: KvantProject.objects.filter(
                id__in=ActiveKvantProject.objects.values_list('project__id', flat=True)).exclude(
                id__in=MemberHiringKvantProject.objects.values_list('project__project__id', flat=True)),
            
            'hiring': lambda: KvantProject.objects.filter(
                id__in=MemberHiringKvantProject.objects.values_list('project__project__id', flat=True)),
        }
        if self.filter_type in project_data.keys():
            return self._subjectQueryFilter(project_data[self.filter_type]())
        return KvantProject.objects.none()
    
    
    def _subjectQueryFilter(self, query):
        if self.subject == 'all':
            return query.all()
        
        elif self.subject == 'mine':
            tutor = query.filter(tutor=self.user)
            teamleader = query.filter(teamleader=self.user)
            team = query.filter(team__id=self.user.id)
            
            return (tutor | teamleader | team).distinct()
        
        return query.filter(course_subject__name=self.subject)


class TaskManipulationManager(ObjectManipulationManager):
    def createTaskProject(self, request, project):
        task_or_errors = self._getCreatedObject(request)
        if isinstance(task_or_errors, KvantProjectTask):
            project.tasks.add(task_or_errors)
        return self.getResponse(task_or_errors)

    def _constructRedirectUrl(self, obj):
        return rl('task_view', kwargs={'task_identifier': obj.id})


class ProjectManipulationManager(ObjectManipulationManager):
    def createProject(self, request):
        project_or_errors = self._getCreatedObject(request)
        if isinstance(project_or_errors, KvantProject):
            ActiveKvantProject.objects.create(project=project_or_errors)
        return self.getResponse(project_or_errors)

    def _constructRedirectUrl(self, obj):
        return rl('project_info', kwargs={'project_identifier': obj.id})


class ApplicationManipulationManager(ObjectManipulationManager):
    """ КОСТЫЛЬ! ПЕРЕДЕЛАЙ! """
    def __init__(self, forms, project, object=None):
        super().__init__(forms, object)
        self.project = project
    
    def createProjectApplication(self, request):
        app_or_errors = self._getCreatedObject(request)
        if isinstance(app_or_errors, KvantProjectMembershipRequest):
            self.project.requests.add(app_or_errors)
        return self.getResponse(app_or_errors)
    
    def _constructRedirectUrl(self, obj):
        return rl('project_info', kwargs={'project_identifier': self.project.project.project.id})


def updateTaskContext(project):
    return {
        'backlog': project.tasks.filter(type='Бэклог'),
        'tasks': project.tasks.filter(type='Задачи'),
        'in_progress': project.tasks.filter(type='В прогрессе'),
        'completed': project.tasks.filter(type='Выполнено'),
        'archive': project.tasks.filter(type='Архив'),
    }


def getTaskById(task_id):
    return KvantProjectTask.objects.get(id=task_id)


def getClassedProject(project):
    if hasattr(project, 'activekvantproject'):
        return project.activekvantproject
    return project.closedkvantproject


def getProjectById(project_id):
    return KvantProject.objects.get(id=project_id)


def getProjectByTaskId(task_id):
    return KvantProject.objects.get(tasks__id=task_id)


def getProjectTeam(task):
    project = KvantProject.objects.get(tasks__id=task.id)
    return {'team': project.team.all(), 'teamleader': project.teamleader}


def getRequestById(request_id):
    return KvantProjectMembershipRequest.objects.get(id=request_id)
