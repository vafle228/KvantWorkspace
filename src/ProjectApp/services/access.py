from CoreApp.services.access import KvantObjectExistsMixin
from ProjectApp.models import KvantProject, KvantProjectTask
from .services import getProjectById, getProjectByTaskId


class KvantProjectExistsMixin(KvantObjectExistsMixin):
    request_object_arg = 'project_identifier'

    def _objectExiststTest(self, object_id):
        return KvantProject.objects.filter(id=object_id).exists()


class ProjectWorkspaceAccessMixin(KvantProjectExistsMixin):
    def accessTest(self, **kwargs):
        if super().accessTest(**kwargs):
            project = getProjectById(kwargs.get(self.request_object_arg))
            return self._projectAccessTest(project, kwargs.get('user'))
        return False

    def _projectAccessTest(self, project, user):
        return (project.tutor == user) or (project.teamleader == user) or (user in project.team.all())


class ProjectTaskAccessMixin(KvantObjectExistsMixin):
    request_object_arg = 'task_identifier'

    def accessTest(self, **kwargs):
        if super().accessTest(**kwargs):
            project = getProjectByTaskId(kwargs.get(self.request_object_arg))
            return self._projectAccessTest(project, kwargs.get('user'))
        return False
    
    def _objectExiststTest(self, object_id):
        return KvantProjectTask.objects.filter(id=object_id).exists()

    def _projectAccessTest(self, project, user):
        return (project.tutor == user) or (project.teamleader == user) or (user in project.team.all())


class ProjectTaskCreateMixin(KvantObjectExistsMixin):
    request_object_arg = 'project_identifier'

    def accessTest(self, **kwargs):
        if super().accessTest(**kwargs):
            project = getProjectById(kwargs.get(self.request_object_arg))
            return self._projectAccessTest(project, kwargs.get('user')) and self._isOpenProjectTest(project)
        return False
    
    def _projectAccessTest(self, project, user):
        return (project.tutor == user) or (project.teamleader == user)
    
    def _objectExiststTest(self, object_id):
        return KvantProject.objects.filter(id=object_id).exists()
    
    def _isOpenProjectTest(self, project):
        return not hasattr(project, 'closedkvantproject')


class ProjectTaskUpdateMixin(KvantObjectExistsMixin):
    request_object_arg = 'task_identifier'

    def accessTest(self, **kwargs):
        if super().accessTest(**kwargs):
            project = getProjectByTaskId(kwargs.get(self.request_object_arg))
            return self._projectAccessTest(project, kwargs.get('user')) and self._isOpenProjectTest(project)
        return False
    
    def _objectExiststTest(self, object_id):
        return KvantProjectTask.objects.filter(id=object_id).exists()

    def _projectAccessTest(self, project, user):
        return (project.tutor == user) or (project.teamleader == user)
    
    def _isOpenProjectTest(self, project):
        return not hasattr(project, 'closedkvantproject')


class ProjectTaskChangeStatusMixin(ProjectTaskUpdateMixin):
    def _projectAccessTest(self, project, user):
        return (project.tutor == user) or (project.teamleader == user) or (user in project.team.all())