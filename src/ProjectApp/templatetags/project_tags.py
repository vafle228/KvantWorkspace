from django import template


register = template.Library()


def getProjectType(project):
    if hasattr(project, 'activekvantproject'):
        if hasattr(project.activekvantproject, 'memberhiringkvantproject'):
            return 'Набор участников'
        return 'Активный'
    return 'Закрытый'


def getSelectedBtn(selected_type, selected):
    return 'selected' if selected_type == selected else ''


def getSelectedUser(user, participants):
    return 'selected' if user in participants.all() else ''


def _getUserTasks(project, user):
    return project.tasks.filter(participants__id=user.id)


def getCurrentTasksCount(project, user):
    return _getUserTasks(project, user).filter(type='Задачи').count()


def getInProgressTasksCount(project, user):
    return _getUserTasks(project, user).filter(type='В прогрессе').count()


def getCompletedTasksCount(project, user):
    return _getUserTasks(project, user).filter(type='Выполнено').count()


def isApplicationExists(project, user):
    return project.requests.filter(sender__id=user.id).exists()


def getApplication(project, user):
    return project.requests.get(sender__id=user.id)


def projectRelated(user, project):
    return (project.tutor == user) or (project.teamleader == user) or (user in project.team.all())


register.filter('get_type', getProjectType)
register.filter('project_related', projectRelated)
register.filter('get_selected_btn', getSelectedBtn)
register.filter('get_selected_user', getSelectedUser)

register.filter('get_current', getCurrentTasksCount)
register.filter('get_completed', getCompletedTasksCount)
register.filter('get_inprogress', getInProgressTasksCount)

register.filter('get_application', getApplication)
register.filter('application_exists', isApplicationExists)
