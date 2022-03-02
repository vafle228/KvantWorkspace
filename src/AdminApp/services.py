from this import d
from .models import KvantCourse


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
