from DiaryApp.models import KvantLesson, KvantTaskBase
from CoreApp.services.access import KvantObjectExistsMixin
from AdminApp.models import KvantCourse
from AdminApp.services import getCourseById
from .queryget import getLessonById, getBaseType


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
        return lesson.course.teacher == user


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
        return course.teacher == user

    def _objectExiststTest(self, object_id):
        return KvantCourse.objects.filter(id=object_id).exists()


class KvantBaseAccessMixin(KvantObjectExistsMixin):
    """ Рассширение для проверки доступа редактирования KvantTaskBase """
    request_object_arg = 'base_identifier'
    
    def accessTest(self, **kwargs):
        if super().accessTest(**kwargs):
            base = KvantTaskBase.objects.get(id=kwargs.get(self.request_object_arg))
            return self._teacherAccessTest(kwargs.get('user'), base)
        return False

    def _objectExiststTest(self, object_id):
        return KvantTaskBase.objects.filter(id=object_id).exists()
    
    def _teacherAccessTest(self, user, base):
        """ Тест на доступ к уроку/заданию """
        if getBaseType(base) == 'lesson':
            return base.kvantlesson.course.teacher == user
        return KvantLesson.objects.get(tasks__base=base).course.teacher == user
