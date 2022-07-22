from CoreApp.services.utils import ObjectManipulationManager
from django.urls import reverse_lazy as rl
from LoginApp.services import getUserById
from NotificationApp.models import (ProjectApplication, ProjectTaskCreate,
                                    ProjectTaskUpdate)
from NotificationApp.services import NotificationBaseManger
from ProjectApp.forms import KvantProjectTypeSaveForm
from ProjectApp.models import (ActiveKvantProject, ClosedKvantProject,
                               KvantProject, KvantProjectMembershipRequest,
                               KvantProjectTask, MemberHiringKvantProject)


class KvantProjectQuerySelector:
    def __init__(self, user, params):
        self.user = user
        
        self.search_param = params.get('search')
        self.subject = params.get('subject') or 'all'
        self.filter_type = params.get('filter') or 'all'
        
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
            return (query.filter(tutor=self.user) | \
                    query.filter(teamleader=self.user) | \
                    query.filter(team__id=self.user.id)).distinct()
        return query.filter(course_subject__name=self.subject)


class TaskManipulationManager(ObjectManipulationManager, NotificationBaseManger):
    def __init__(self, forms, object=None):
        if KvantProjectTypeSaveForm in forms:
            self._notify = lambda **x: x  # Чисто заглушка
        super().__init__(forms, object)
    
    def createTaskProject(self, request, project):
        task_or_errors = self._getCreatedObject(request)
        
        if isinstance(task_or_errors, KvantProjectTask):
            project.tasks.add(task_or_errors)
            self._notify(
                task=task_or_errors, sender=request.user,
                model=ProjectTaskCreate, project=project,
            )  
        return self.getResponse(task_or_errors, project=project)
    
    def updateTaskProject(self, request, project):
        task_or_errors = self._getUpdatedObject(request)

        if isinstance(task_or_errors, KvantProjectTask):
            self._notify(
                task=task_or_errors, sender=request.user,
                model=ProjectTaskUpdate, project=project
            )
        return self.getResponse(task_or_errors, project=project)
    
    def _notify(self, **kwargs):
        for receiver in getProjectUsers(kwargs.get('project')):
            if receiver == kwargs.get('sender'):
                continue
            self.broadcastNotification(**kwargs, receiver=receiver)
    
    def buildBase(self, **kwargs):
        project_kwargs = {
            'task': kwargs.get('task'),
            'sender': kwargs.get('sender'),
            'receiver': kwargs.get('receiver'),    
        }

        if kwargs.get('model') == ProjectTaskUpdate:
            if ProjectTaskUpdate.objects.filter(**project_kwargs).exists():
                ProjectTaskUpdate.objects.get(**project_kwargs).delete()
        return kwargs.get('model').objects.create(**project_kwargs)

    def _constructRedirectUrl(self, **kwargs):
        return rl('task_view', kwargs={
            'task_identifier': kwargs.get('obj').id,
            'project_identifier': kwargs.get('project').id
        })


class ProjectManipulationManager(ObjectManipulationManager):
    def createProject(self, request):
        project_or_errors = self._getCreatedObject(request)
        if isinstance(project_or_errors, KvantProject):
            ActiveKvantProject.objects.create(project=project_or_errors)
        return self.getResponse(project_or_errors)

    def _constructRedirectUrl(self, **kwargs):
        return rl('project_info', kwargs={'project_identifier': kwargs.get('obj').id})


class ApplicationManipulationManager(ObjectManipulationManager, NotificationBaseManger):    
    def createProjectApplication(self, request, project):
        app_or_errors = self._getCreatedObject(request)
        if isinstance(app_or_errors, KvantProjectMembershipRequest):
            project.requests.add(app_or_errors)
            
            for receiver in getProjectUsers(project.project.project):
                self.broadcastNotification(application=app_or_errors, receiver=receiver)

        return self.getResponse(app_or_errors, project=project.project.project)
    
    def buildBase(self, **kwargs):
        return ProjectApplication.objects.create(**kwargs)
    
    def _constructRedirectUrl(self, **kwargs):
        return rl('project_info', kwargs={'project_identifier': kwargs.get('project').id})


class ProjectStatusManager:
    def __init__(self, project):
        self.project = project
    
    def hiringStatusManager(self, choise):
        if choise == 'on' and isinstance(self.project, ActiveKvantProject):
            return MemberHiringKvantProject.objects.create(project=self.project)
        elif MemberHiringKvantProject.objects.filter(project=self.project).exists():
            return MemberHiringKvantProject.objects.get(project=self.project).delete()
    
    def closeProjectManager(self):
        project_instance = self._getProjectInstance()
        self._deleteProjectStatus()
        
        return ClosedKvantProject.objects.create(project=project_instance)
    
    def _getProjectInstance(self):
        if isinstance(self.project, MemberHiringKvantProject):
            return self.project.project.project
        return self.project.project
    
    def _deleteProjectStatus(self):
        if isinstance(self.project, MemberHiringKvantProject):
            return self.project.project.delete()
        return self.project.delete()


class ProjectTeamManager:
    def __init__(self, project):
        self.project = project
    
    def projectMemeberJoin(self, application, choise):
        if choise == 'accept':
            self.project.team.add(application.sender)
        application.delete()
    
    def projectMemberKick(self, user_id):
        user = getUserById(user_id)
        if user is not None:
            self.project.team.remove(user)
            self._cleanUserTasks(user)
            
    def _cleanUserTasks(self, user):
        for task in self.project.tasks.filter(participants__id=user.id):
            task.participants.remove(user)
    
    def changeTeamleader(self, user):
        if user == self.project.teamleader: return 
        
        self.project.team.remove(user)
        self.project.team.add(self.project.teamleader)
        self.project.teamleader = user
        
        self.project.save()


def updateTaskContext(project):
    return {
        'backlog': project.tasks.filter(type='Бэклог'),
        'tasks': project.tasks.filter(type='Задачи'),
        'in_progress': project.tasks.filter(type='В прогрессе'),
        'completed': project.tasks.filter(type='Выполнено'),
        'archive': project.tasks.filter(type='Архив'),
    }


def getClassedProject(project):
    if hasattr(project, 'activekvantproject'):
        return project.activekvantproject
    return project.closedkvantproject


def getTaskById(task_id):
    return KvantProjectTask.objects.get(id=task_id)


def getProjectById(project_id):
    return KvantProject.objects.get(id=project_id)


def getRequestById(request_id):
    return KvantProjectMembershipRequest.objects.get(id=request_id)


def getProjectUsers(project):
    return [
        project.tutor, project.teamleader,
    ] + [student for student in project.team.all()]
