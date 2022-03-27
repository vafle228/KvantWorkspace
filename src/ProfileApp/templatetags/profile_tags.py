from django import template
from AdminApp.services import getCourseQuery
from DiaryApp.models import KvantLesson


register = template.Library()


def getLessonByCourse(course):
    return KvantLesson.objects.filter(course=course)


register.filter('get_lesson', getLessonByCourse)
register.filter('get_user_courses', getCourseQuery)
