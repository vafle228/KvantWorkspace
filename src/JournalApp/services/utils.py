from json import loads

from CoreApp.services.utils import (ObjectManipulationManager,
                                    ObjectManipulationResponse)
from DiaryApp.models import KvantHomeTask, KvantTaskBase, KvantTaskMark
from django.urls import reverse_lazy as rl
from JournalApp.forms import KvantMarkSaveForm
from LoginApp.services import getUserById
from NotificationApp.forms import TaskNotificationSaveForm
from NotificationApp.services import NotificationBaseManger

from .queryget import getBaseStudents, getBaseType
from datetime import datetime


class KvantTaskManager(ObjectManipulationManager, NotificationBaseManger):
    """ 
    Создает задание для урока, наследуя ObjectManipulationManager.
    Реализует закрепление за уроком, по средствам проверки сущности.
    """
    def createKvantTask(self, request, lesson):
        base_or_error = self._getCreatedObject(request)
        if isinstance(base_or_error, KvantTaskBase):
            task = KvantHomeTask.objects.create(base=base_or_error)
            lesson.tasks.add(task)
            
            for student in lesson.course.students.all():
                self.broadcastNotification(task=task, receiver=student)
        return self.getResponse(base_or_error)
    
    def buildNotification(self, **kwargs):
        form = TaskNotificationSaveForm({
            'task_obj': kwargs.get('task'),
            'receiver': kwargs.get('receiver'),
            'redirect_link': f"{rl('diary_page')}?period={datetime.now().month}",
        })
        return form.save() if form.is_valid() else None
    
    def _constructRedirectUrl(self, obj):
        return rl('checking_page', kwargs={'base_identifier': obj.id})


class KvantBaseMarksUpdate(ObjectManipulationResponse):
    """ 
    Создает отметки и возвращает JSON Response.
    Наследует ObjectManipulationResponse для генерации JSON Response.
    """
    def __init__(self, request):
        self.marks = loads(request.POST['marks'])
    
    def createKvantMarks(self, base):
        """ 
        Иттерирует все переданные отметки.
        Вызывает getResponse для перенаправления на checking_page
        """
        for student_id in self.marks.keys():
            self._manageMark(student_id, base)
        return self.getResponse(base)
    
    def _constructRedirectUrl(self, **kwargs):
        return rl('checking_page', kwargs={'base_identifier': kwargs.get('obj').id})

    def _manageMark(self, student_id, base):
        """ Создает отметки. Если отметка - '', удаляет ее """
        if self.marks[student_id] == '': 
            return self._deleteMark(student_id, base)
        
        mark_instance = self._getMarkInstance(base, student_id)
        mark_or_errors = self._createMark(student_id, self.marks[student_id], mark_instance)
        
        if isinstance(mark_or_errors, KvantTaskMark): return base.marks.add(mark_or_errors)

    def _deleteMark(self, student_id, base):
        """ Удаляет созданные ранее отметки """
        student_user = getUserById(student_id)
        if base.marks.filter(student=student_user).exists():
            base.marks.get(student=student_user).delete()
    
    def _getMarkInstance(self, base, student_id):
        """ Получает отметку base по student_id """
        student_user = getUserById(student_id)
        if base.marks.filter(student=student_user).exists():
            return base.marks.get(student=student_user)
        return None

    def _createMark(self, student_id, mark, mark_instance):
        """ Создает отметки. Возвращяет отметку или ошибки """
        form = KvantMarkSaveForm(
            {'student': student_id, 'mark': mark}, instance=mark_instance)
        return form.save() if form.is_valid() else form.errors


class KvantBaseStatistic:
    def __init__(self, base):
        self.base = base
    
    def countWorkComplete(self):
        if getBaseType(self.base) == 'lesson':
            return self._calculateAttendance()
        return self._calculateWorkCount()
    
    def countWorkQuality(self):
        if getBaseType(self.base) == 'lesson':
            return self._calculatePureAttendance()
        return self._calculateWorkQuality()
    
    def _calculateAttendance(self):
        all_students = len(getBaseStudents(self.base))
        miss_count = len(self.base.marks.filter(mark='ОТ'))

        return '0%' if all_students == 0 else f'{int((all_students - miss_count) / all_students * 100)}%'
    
    def _calculateWorkCount(self):
        all_students = len(getBaseStudents(self.base))
        work_count = len(self.base.kvanthometask.works.all())

        return '0%' if all_students == 0 else f'{int(work_count / all_students * 100)}%'
    

    def _calculateWorkQuality(self):
        max_sum = len(getBaseStudents(self.base)) * 4
        mark_sum = sum([int(mark.mark) for mark in self.base.marks.all()])

        return '0%' if max_sum == 0 else f'{int(mark_sum / max_sum * 100)}%'
    

    def _calculatePureAttendance(self):
        all_students = len(getBaseStudents(self.base))
        reasonable_count = len(self.base.marks.filter(mark='УП'))

        return '0%' if all_students == 0 else f'{int(reasonable_count / all_students * 100)}%'
