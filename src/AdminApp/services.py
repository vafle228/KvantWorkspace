import datetime as dt

import openpyxl as px
from CoreApp.services.utils import ObjectManipulationManager
from django.urls import reverse_lazy as rl
from JournalApp.forms import KvantBaseSaveForm, KvantLessonSaveForm
from LoginApp.models import KvantUser
from RegisterApp.models import StaffPersonalInfo, StudentPersonalInfo
from RegisterApp.serializers import (StaffPersonalInfoSerializer,
                                     StudentPersonalInfoSerializer)

from .models import KvantCourse, KvantCourseType


class CourseSubjectManipulationManager(ObjectManipulationManager):
    def _constructRedirectUrl(self, **kwargs):
        return rl('subjects_table')


class CourseManipulationManager(ObjectManipulationManager):
    def createCourse(self, request):
        today = dt.datetime.now()
        course_or_errors = self._getCreatedObject(request)
        
        if isinstance(course_or_errors, KvantCourse):
            for schedule in course_or_errors.schedule.all():
                days_delta = self._getDaysDelta(today, self._getWeekDayNumber(schedule.week_day))
                dates = self._generateLessonsDates(today + dt.timedelta(days=days_delta))
                for i in range(len(dates)):
                    self._createLesson(dates[i], f'Урок на {dates[i].date()} #{i}', course_or_errors, schedule.time)
        return self.getResponse(course_or_errors)
    
    def _getDaysDelta(self, today, lesson_day):
        if today.weekday() >= lesson_day:
            return (lesson_day + 7) - today.weekday()
        return lesson_day - today.weekday()

    def _getWeekDayNumber(self, weekday):
        return {'ПН': 0, 'ВТ': 1,
                'СР': 2, 'ЧТ': 3,
                'ПТ': 4, 'СБ': 5,
                'ВС': 6}.get(weekday)
    
    def _generateLessonsDates(self, nearest_lesson):
        if 6 <= nearest_lesson.month <= 8:
            return [None]

        lessons = [nearest_lesson]
        next_lesson = nearest_lesson + dt.timedelta(days=7)
        while next_lesson.month > 8 or next_lesson.month < 6:
            lessons.append(next_lesson)
            next_lesson = next_lesson + dt.timedelta(days=7)
        return lessons
    
    def _createLesson(self, date, name, course, time):
        base = self._createLessonBase(name)
        
        if base is not None:
            form = KvantLessonSaveForm({
                'date': date, 'base': base, 
                'course': course, 'time': time,
            })
            return form.save() if form.is_valid() else None
    
    def _createLessonBase(self, name):
        form = KvantBaseSaveForm({'title': name})
        return form.save() if form.is_valid() else None

    def _constructRedirectUrl(self, **kwargs):
        return rl('courses_table')


class PersonalInfoExcelImport:
    def __init__(self):
        self._wb = px.Workbook()
        self._ws = self._wb.active
    
    def importPersonalInfo(self, user_type):
        if user_type == 'Ученик':
            return self._importStudentPersonalInfo()
        return self._importStaffPersonalInfo()
    
    def _importStudentPersonalInfo(self):
        for student in StudentPersonalInfo.objects.all():
            print(StudentPersonalInfoSerializer(student).data)

    def _importStaffPersonalInfo(self):
        pass


def getCourseById(course_id):
    """ Возвращает курс по его course_id """
    return KvantCourse.objects.get(id=course_id)


def getCourseQuery(user):
    """ Получает множество курсов основываясь на user """
    return {
        'Ученик': lambda user: KvantCourse.objects.filter(students__in=[user]),
        'Учитель': lambda user: KvantCourse.objects.filter(teacher=user),
        'Администратор': lambda user: KvantCourse.objects.none(),
    }[user.permission](user)


def getCourseTypeQuery(user):
    types = []
    for course in getCourseQuery(user):
        types.append(course.type.name)
    return set(types)


allCourses = lambda: KvantCourse.objects.all()
allSubjects = lambda: KvantCourseType.objects.all()
allUsers = lambda permission: KvantUser.objects.filter(permission=permission)
