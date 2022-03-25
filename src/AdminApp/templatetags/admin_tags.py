from django import template
from AdminApp.models import KvantCourse


register = template.Library()


def getTypedCourses(subject):
    return KvantCourse.objects.filter(type=subject)


def getTypedCourseCount(subject):
    return getTypedCourses(subject).count()


def getTypedStudentsCount(subject):
    result = 0
    for course in getTypedCourses(subject):
        result += course.students.all().count()
    return result


register.filter('course_count', getTypedCourseCount)
register.filter('student_count', getTypedStudentsCount)
