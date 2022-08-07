from JournalApp.forms import KvantBaseSaveForm, KvantLessonSaveForm
from .models import KvantCourse, KvantCourseType
from LoginApp.models import KvantUser
from CoreApp.services.utils import ObjectManipulationManager
from django.urls import reverse_lazy as rl
import datetime as dt


class CourseSubjectManipulationManager(ObjectManipulationManager):
    def _constructRedirectUrl(self, **kwargs):
        return rl('subjects_table')


class CourseManipulationManager(ObjectManipulationManager):
    def createCourse(self, request):
        today = dt.datetime.now()
        course_or_errors = self._getCreatedObject(request)
        
        if isinstance(course_or_errors, KvantCourse):
            lesson_days = [self._getWeekDayNumber(schedule.week_day) for schedule in course_or_errors.schedule.all()]
            for lesson_day in lesson_days:
                if today.weekday() >= lesson_day:
                    days_delta = (lesson_day + 7) - today.weekday()
                else:
                    days_delta = lesson_day - today.weekday()

                dates = self._generateLessonsDates(today + dt.timedelta(days=days_delta))
                for i in range(len(dates)):
                    self._createLesson(dates[i], f'Урок на {dates[i].date()} #{i}', course_or_errors)
        return self.getResponse(course_or_errors)

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
    
    def _createLesson(self, date, name, course):
        base = self._createLessonBase(name)
        
        if base is not None:
            form = KvantLessonSaveForm({
                'date': date, 'base': base, 'course': course,
            })
            return form.save() if form.is_valid() else None
    
    def _createLessonBase(self, name):
        form = KvantBaseSaveForm({'title': name})
        return form.save() if form.is_valid() else None

    def _constructRedirectUrl(self, **kwargs):
        return rl('courses_table')


def getCourseById(course_id):
    """ Возвращает курс по его course_id """
    return KvantCourse.objects.get(id=course_id)


def getCourseQuery(user):
    """ Получает множество курсов основываясь на user """
    return {
        'Ученик': lambda user: KvantCourse.objects.filter(students=user),
        'Учитель': lambda user: KvantCourse.objects.filter(teacher=user),
        'Администратор': lambda user: KvantCourse.objects.none(),
    }[user.permission](user)


allCourses = lambda: KvantCourse.objects.all()
allSubjects = lambda: KvantCourseType.objects.all()
allUsers = lambda permission: KvantUser.objects.filter(permission=permission)