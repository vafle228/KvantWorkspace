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
    courses = getTypedCourses(subject)
    return len(set([student for course in courses for student in course.students.all()]))


def get_active_shedule(course, day):
    if course.schedule.filter(week_day=day).exists():
        return course.schedule.get(week_day=day)
    return None


def wrapScanObject(file):
    return Wrapper(file)


register.filter('wrap', wrapScanObject)
register.filter('course_count', getTypedCourseCount)
register.filter('student_count', getTypedStudentsCount)
register.filter('get_active_shedule', get_active_shedule)
