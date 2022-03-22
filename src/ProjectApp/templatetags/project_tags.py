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


register.filter('get_type', getProjectType)
register.filter('get_selected_btn', getSelectedBtn)
