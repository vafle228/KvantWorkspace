import datetime as dt

from AdminApp.models import KvantCourse, KvantCourseShedule
from AdminApp.services import allUsers
from DiaryApp.models import KvantLesson, KvantTaskBase
from LoginApp.models import KvantUser
from django.urls import reverse_lazy as rl


def getBaseById(base_id):
    """ Получает KvantBase по его base_id """
    return KvantTaskBase.objects.get(id=base_id)


def getLessonById(lesson_id):
    """ Возвращает урок с заданным lesson_id """
    return KvantLesson.objects.get(id=lesson_id)


def getJournalLessonQuery(course, period):
    """ Возвращает уроки пользователя по заданному course и period """
    if period in ['1', '2']:
        return {
            '1': lambda course: KvantLesson.objects.filter(course=course, date__month__gte=7),
            '2': lambda course: KvantLesson.objects.filter(course=course, date__month__lte=6),
        }[period](course)
    return KvantLesson.objects.none()


def getBaseType(base):
    """ Возвращает тип base в зависимости от аттрибута o2o field """
    return 'lesson' if hasattr(base, 'kvantlesson') else 'task'


def getBaseStudents(base):
    """ Получает всех студентов данной базы """
    if getBaseType(base) == 'lesson':
        return base.kvantlesson.course.students.all()
    return KvantLesson.objects.get(tasks__base=base).course.students.all()


def getSheduleTeachers(choise):
    if choise == 'all':
        return allUsers('Учитель')
    return KvantUser.objects.filter(id=choise)


class CourseSchedule:
    def __init__(self, user, day=None):
        self.day = day
        self.user = user
    
    def getTodaySchedule(self):
        today_schedule = []
        for lesson in sorted(self._getTodayLessons(), key=lambda item: item.date):
            today_schedule.append(
                (lesson.time.strftime("%H:%M"), f'{lesson.course}', 
                lesson.base.title, self._getRedirectLink(lesson))
            )
        return today_schedule
    
    def getCourseSchedule(self):
        courses_schedules = []
        for schedule in sorted(self._getDaySchedule(), key=lambda item: item.time):
            end_time = self._getLessonEnd(schedule.time)
            start_time = schedule.time.strftime("%H:%M")
            course = KvantCourse.objects.get(schedule__in=[schedule], teacher=self.user)

            courses_schedules.append((f'{course}', f'{start_time} - {end_time}'))
        return courses_schedules
    
    def _getTodayLessons(self):
        if self.user.permission == 'Администратор':
            return
        
        lessons = KvantLesson.objects.filter(date=dt.datetime.today(), time__gte=dt.datetime.today())
        if self.user.permission == 'Ученик':
            return lessons.filter(course__students__in=[self.user])
        return lessons.filter(course__teacher=self.user)
    
    def _getRedirectLink(self, lesson):
        if self.user.permission == 'Администратор':
            return
        
        month = dt.datetime.today().month
        if self.user.permission == 'Ученик':
            return f"{rl('diary_page')}?period={month}&lesson={lesson.id}"
        return rl('checking_page', kwargs={'base_identifier': lesson.base.id})
            
    
    def _getDaySchedule(self):
        return KvantCourseShedule.objects.filter(week_day=self.day, kvantcourse__teacher=self.user)
    
    def _getLessonEnd(self, start):
        return (dt.datetime.combine(dt.date(1,1,1), start) + dt.timedelta(minutes=100)).strftime("%H:%M")
