from .models import KvantCourse, KvantCourseType
from LoginApp.models import KvantUser
from CoreApp.services.utils import ObjectManipulationManager
from django.urls import reverse_lazy as rl


class CourseSubjectManipulationManager(ObjectManipulationManager):
    def _constructRedirectUrl(self, **kwargs):
        return rl('subjects_table')


def getCourseById(course_id):
    """ Возвращает курс по его course_id """
    return KvantCourse.objects.get(id=course_id)


def getCourseQuery(user):
    """ Получает множество курсов основываясь на user """
    return {
        'Ученик': lambda user: KvantCourse.objects.filter(students=user),
        'Учитель': lambda user: KvantCourse.objects.filter(teacher=user),
        'Администратор': lambda user: KvantCourse.objects.all(),
    }[user.permission](user)


allCourses = lambda: KvantCourse.objects.all()
allSubjects = lambda: KvantCourseType.objects.all()
allUsers = lambda permission: KvantUser.objects.filter(permission=permission)