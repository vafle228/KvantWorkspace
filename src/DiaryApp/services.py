from DiaryApp.models import KvantLesson, KvantHomeTask, KvantHomeWork
from CoreApp.services.access import KvantObjectExistsMixin
from JournalApp.services.queryget import getLessonById
from CoreApp.services.utils import ObjectManipulationManager
from django.urls import reverse_lazy as rl
from CoreApp.services.access import KvantStudentAccessMixin


def getTaskById(task_id):
    """ Возвращает задание по переданному task_id """
    return KvantHomeTask.objects.get(id=task_id)

def getDiaryLessonQuery(user, period):
    """ Возвращает уроки ученика user за дату period """
    return KvantLesson.objects.filter(course__students=user, date__month=period)


def getUserWork(task, user):
    """ 
    Получает работу user в задании task.
    Возвращает None, если работы нет 
    """
    if task.works.all().filter(sender=user).exists():
        return task.works.all().get(sender=user)
    return None

def getWorkById(work_id):
    """ Получает работу по work_id """
    return KvantHomeWork.objects.get(id=work_id)


class DiaryPaginator:
    def generateNext(self, period):
        return rl('diary_page') + f'?period={period % 12 + 1}'
    
    def generatePrev(self, period):
        return rl('diary_page') + f'?period={(period - 1) + 12 * int(not period - 1)}' 


class HomeWorkManipulationManager(ObjectManipulationManager):
    def createTaskWork(self, request):
        task = getTaskById(request.POST.get('task_id'))
        work_or_errors = self._getCreatedObject(request)

        if isinstance(work_or_errors, KvantHomeWork):
            task.works.add(work_or_errors)
        return self.getResponse(work_or_errors)

    def _constructRedirectUrl(self, obj):
        return rl('task_detail', kwargs={
            'task_identifier': KvantHomeTask.objects.get(works__id=obj.id).id
        })

class DiaryMonthValidateMixin(KvantStudentAccessMixin):
    def accessTest(self, **kwargs):
        month_num = kwargs.get('month_num')
        return super().accessTest(**kwargs) and self._validateMonth(month_num)
    
    def _validateMonth(self, month_num):
        if month_num and month_num.isdigit():
            return 1 <= int(month_num) <= 12
        return False

class LessonAccessMixin(KvantObjectExistsMixin):
    request_object_arg = 'lesson_identifier'

    def accessTest(self, **kwargs):
        if super().accessTest(**kwargs):
            lesson = getLessonById(kwargs.get(self.request_object_arg))
            return self._lessonAccessMixin(lesson, kwargs.get('user'))
        return False
    
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
        return False

    def _objectExiststTest(self, object_id):
        return KvantHomeTask.objects.filter(id=object_id).exists()
    
    def _taskAccessMixin(self, task, user):
        return user in KvantLesson.objects.get(tasks__id=task.id).course.students.all()


class WorkEditAccessMixin(KvantObjectExistsMixin):
    request_object_arg = 'work_identifier'

    def accessTest(self, **kwargs):
        if super().accessTest(**kwargs):
            work = getWorkById(kwargs.get(self.request_object_arg))
            return self._workAccessTest(work, kwargs.get('user'))
        return False
    
    def _objectExiststTest(self, object_id):
        return KvantHomeWork.objects.filter(id=object_id).exists()
    
    def _workAccessTest(self, work, user):
        return work.sender == user