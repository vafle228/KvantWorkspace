from DiaryApp.models import KvantLesson, KvantHomeTask, KvantHomeWork
from CoreApp.services.access import KvantObjectExistsMixin
from JournalApp.services.queryget import getLessonById
from CoreApp.services.utils import ObjectManipulationManager
from django.urls import reverse_lazy as rl
from CoreApp.services.access import KvantStudentAccessMixin

from NotificationApp.services import NotificationBaseManger
from NotificationApp.models import WorkCreateNotification, WorkUpdateNotification


def getTaskById(task_id):
    """ Возвращает задание по переданному task_id """
    return KvantHomeTask.objects.get(id=task_id)

def getDiaryLessonQuery(user, period):
    """ Возвращает уроки ученика user за дату period """
    return sorted(
        KvantLesson.objects.filter(course__students=user, date__month=period), 
        key=lambda item: (item.date, item.time)
    )

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


class HomeWorkManipulationManager(ObjectManipulationManager, NotificationBaseManger):
    def createTaskWork(self, request):
        work_or_errors = self._getCreatedObject(request)

        if isinstance(work_or_errors, KvantHomeWork):
            task = getTaskById(request.POST.get('task_id')); task.works.add(work_or_errors)
            
            self.broadcastNotification(
                work=work_or_errors, model=WorkCreateNotification,
                receiver=KvantLesson.objects.get(tasks__base=task.base).course.teacher
            )
        return self.getResponse(work_or_errors)
    
    def updateObject(self, request):
        work_or_errors = self._getUpdatedObject(request)

        if isinstance(work_or_errors, KvantHomeWork):
            task = KvantHomeTask.objects.get(works__id=work_or_errors.id)

            self.broadcastNotification(
                work=work_or_errors, model=WorkUpdateNotification,
                receiver=KvantLesson.objects.get(tasks__base=task.base).course.teacher
            )
        return self.getResponse(work_or_errors)
    
    def buildBase(self, **kwargs):
        obj_args = {
            'work': kwargs.get('work'),
            'receiver': kwargs.get('receiver'),
        }

        if kwargs.get('model') == WorkUpdateNotification:
            if WorkUpdateNotification.objects.filter(**obj_args).exists():
                WorkUpdateNotification.objects.filter(**obj_args).first().delete()
        return kwargs.get('model').objects.create(**obj_args)

    def _constructRedirectUrl(self, **kwargs):
        return rl('task_detail', kwargs={
            'task_identifier': KvantHomeTask.objects.get(works__id=kwargs.get('obj').id).id
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