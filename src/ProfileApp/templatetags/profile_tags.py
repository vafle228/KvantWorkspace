from AdminApp.services import getCourseQuery, getCourseTypeQuery
from DiaryApp.models import KvantLesson
from django import template

register = template.Library()


def getLessonByCourse(course):
    return KvantLesson.objects.filter(course=course)


register.filter('get_lesson', getLessonByCourse)
register.filter('get_user_courses', getCourseQuery)
register.filter('get_user_courses_types', getCourseTypeQuery)
