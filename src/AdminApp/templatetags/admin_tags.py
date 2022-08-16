from django import template
from AdminApp.models import KvantCourse


register = template.Library()


class Wrapper:
    def __init__(self, file):
        self.file = file
    
    def all(self):
        return [self]


def getTypedCourses(subject):
    return KvantCourse.objects.filter(type=subject)


def getTypedCourseCount(subject):
    return getTypedCourses(subject).count()


def getTypedStudentsCount(subject):
    result = 0
    for course in getTypedCourses(subject):
        result += course.students.all().count()
    return result


def wrapScanObject(file):
    return Wrapper(file)


register.filter('wrap', wrapScanObject)
register.filter('course_count', getTypedCourseCount)
register.filter('student_count', getTypedStudentsCount)
