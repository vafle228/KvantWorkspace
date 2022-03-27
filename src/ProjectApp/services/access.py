from CoreApp.services.access import (KvantObjectExistsMixin,
                                     KvantStudentAccessMixin)
from ProjectApp.models import (KvantProject, KvantProjectTask,
                               KvantProjectMembershipRequest)

from .services import getProjectById


class KvantProjectExistsMixin(KvantObjectExistsMixin):
    request_object_arg = 'project_identifier'

    def _objectExiststTest(self, object_id):
        return KvantProject.objects.filter(id=object_id).exists()


class KvantProjectManageMixin(KvantProjectExistsMixin):
    def accessTest(self, **kwargs):
        if super().accessTest(**kwargs):
            project = getProjectById(kwargs.get(self.request_object_arg))
            return self._teamManageAccessTest(project, kwargs.get('user'))
        return False
    
    def _teamManageAccessTest(self, project, user):
        return (project.tutor == user) or (project.teamleader == user)


class ProjectWorkspaceAccessMixin(KvantProjectExistsMixin):
    project_arg = 'project_identifier'

    def accessTest(self, **kwargs):
        if super().accessTest(**kwargs):
            project = getProjectById(kwargs.get(self.project_arg))
            return self._projectAccessTest(project, kwargs.get('user')) or self._projectAvaliableTest(project)
        return False
    
    def _projectAccessTest(self, project, user):
        return (project.tutor == user) or (project.teamleader == user) or (user in project.team.all())
    
    def _projectAvaliableTest(self, project):
        return hasattr(project, 'closedkvantproject')


class ProjectTaskAccessMixin(ProjectWorkspaceAccessMixin):
    task_object_arg = 'task_identifier'

    def accessTest(self, **kwargs):
        if super().accessTest(**kwargs):
            return self._taskExiststTest(kwargs.get(self.task_object_arg))
        return False

    def _taskExiststTest(self, object_id):
        return KvantProjectTask.objects.filter(id=object_id).exists()


class ProjectTaskManipulationMixin(ProjectTaskAccessMixin):
    def accessTest(self, **kwargs):
        if super().accessTest(**kwargs):
            project = getProjectById(kwargs.get(self.project_arg))
            return self._projectActiveTest(project)
        return False

    def _projectActiveTest(self, project):
        return not hasattr(project, 'closedkvantproject')
    

class ProjectApplicationCreateMixin(KvantProjectExistsMixin, KvantStudentAccessMixin):
    pass


class ProjectApplicationManageMixin(KvantProjectManageMixin):
    application_object_arg = 'application_identifier'

    def accessTest(self, **kwargs):
        if super().accessTest(**kwargs):
            return self._requestExiststTest(kwargs.get(self.application_object_arg))
        return False

    def _requestExiststTest(self, object_id):
        return KvantProjectMembershipRequest.objects.filter(id=object_id).exists() 
