from DiaryApp.models import KvantLesson, KvantHomeTask
from CoreApp.services.access import KvantObjectExistsMixin
from JournalApp.services.queryget import getLessonById


def getTaskById(self, task_id):
    """ Возвращает задание по переданному task_id """
    return KvantHomeTask.objects.get(id=task_id)

def getDiaryLessonQuery(user):
    """ Возвращает уроки ученика """
    return KvantLesson.objects.filter(course__students=user)


class LessonAccessMixin(KvantObjectExistsMixin):
    request_object_arg = 'lesson_identifier'

    def accessTest(self, **kwargs):
        if super().accessTest(**kwargs):
            lesson = getLessonById(kwargs.get(self.request_object_arg))
            return self._lessonAccessMixin(lesson, kwargs.get('user'))
    
    def _objectExiststTest(self, object_id):
        return KvantLesson.objects.filter(id=object_id).exists()
    
    def _lessonAccessMixin(self, lesson, user):
        return user in lesson.course.students.all()


class TaskAccessMixin(KvantObjectExistsMixin):
    request_object_arg = 'task_identifier'

    def accessTest(self, **kwargs):
        if super().accessTest(**kwargs):
            task = getTaskById(kwargs.get(self.request_object_arg))
            return self._taskAccessMixin(task, kwargs.get('user'))

    def _objectExiststTest(self, object_id):
        return KvantHomeTask.objects.filter(id=object_id).exists()
    
    def _taskAccessMixin(self, task, user):
        return task.sender == user
