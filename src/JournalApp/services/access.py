from AdminApp.models import KvantCourse
from AdminApp.services import getCourseById
from CoreApp.services.access import (KvantObjectExistsMixin,
                                     KvantTeacherAndAdminAccessMixin)
from DiaryApp.models import KvantLesson, KvantTaskBase
from LoginApp.models import KvantUser

from .queryget import getBaseById, getBaseType, getLessonById


class KvantLessonAccessMixin(KvantObjectExistsMixin):
    """ Рассширение для проверки доступа редактирования урока """
    request_object_arg = 'lesson_identifier'

    def accessTest(self, **kwargs):
        if super().accessTest(**kwargs):
            lesson = getLessonById(kwargs.get(self.request_object_arg))
            return self._lessonAccessTest(kwargs.get('user'), lesson)
        return False

    def _objectExiststTest(self, object_id):
        return KvantLesson.objects.filter(id=object_id).exists()
    
    def _lessonAccessTest(self, user, lesson):
        return lesson.course.teacher == user or user.permission == 'Администратор'


class KvantSheduleAccessMixin(KvantObjectExistsMixin, KvantTeacherAndAdminAccessMixin):
    request_object_arg = 'teacher_identifier'

    def accessTest(self, **kwargs):
        if super().accessTest(**kwargs):
            return self._sheduleAccessTest(kwargs.get(self.request_object_arg))
        return False

    def _sheduleAccessTest(self, choise):
        return choise == 'all' or KvantUser.objects.get(id=choise).permission == 'Учитель'

    def _objectExiststTest(self, object_id):
        return object_id == 'all' or KvantUser.objects.filter(id=object_id).exists()


class KvantJournalAccessMixin(KvantObjectExistsMixin):
    """ Рассширение для проверки доступа к журналу """
    request_object_arg = 'course_identifier'

    def accessTest(self, **kwargs):
        if super().accessTest(**kwargs):
            course = getCourseById(kwargs.get(self.request_object_arg))
            return self._journalAccessTest(kwargs.get('user'), course)
        return False

    def _journalAccessTest(self, user, course):
        """ Тест на возможность просматривать курс """
        return course.teacher == user or user.permission == 'Администратор'

    def _objectExiststTest(self, object_id):
        return KvantCourse.objects.filter(id=object_id).exists()


class KvantBaseAccessMixin(KvantObjectExistsMixin):
    """ Рассширение для проверки доступа редактирования KvantTaskBase """
    request_object_arg = 'base_identifier'
    
    def accessTest(self, **kwargs):
        if super().accessTest(**kwargs):
            base = getBaseById(kwargs.get(self.request_object_arg))
            return self._teacherAccessTest(kwargs.get('user'), base) or kwargs.get('user').permission == 'Администратор'
        return False

    def _objectExiststTest(self, object_id):
        return KvantTaskBase.objects.filter(id=object_id).exists()
    
    def _teacherAccessTest(self, user, base):
        """ Тест на доступ к уроку/заданию """
        if getBaseType(base) == 'lesson':
            return base.kvantlesson.course.teacher == user
        return KvantLesson.objects.get(tasks__base=base).course.teacher == user
