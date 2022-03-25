from LoginApp.services import getUserById
from ProjectApp.models import KvantProject
from ProjectApp.services.services import getClassedProject, getProjectById

from .forms import ChatMessageSaveForm


class ChatProjectAccessMixin:
    def __init__(self, user_id, project_id):
        self.user_id = user_id
        self.project_id = project_id
    
    def checkAccess(self):
        user = getUserById(self.user_id)
        if self._authenticateTest(user) and self._objectExiststTest(self.project_id):
            project = getProjectById(self.project_id)
            return self._chatAccessTest(project, user) and self._isActiveProject(project)
        return False
    
    def _authenticateTest(self, user):
        """ Тест на авторизованность """
        return user.is_authenticated
    
    def _objectExiststTest(self, object_id):
        return KvantProject.objects.filter(id=object_id).exists()
    
    def _isActiveProject(self, project):
        return hasattr(project, 'activekvantproject')
    
    def _chatAccessTest(self, project, user):
        return (project.tutor == user) or (project.teamleader == user) or (user in project.team.all())


def addProjectChatMessage(message, user_id, project_id):
    form = ChatMessageSaveForm({
        'sender': getUserById(user_id), 'message': message})
    if form.is_valid():
        chat_instance = form.save()
        project = getProjectById(project_id)
        getClassedProject(project).chat.add(chat_instance)

        return chat_instance
    return form.errors
