import datetime as dt
from collections import OrderedDict

import openpyxl as px
from CoreApp.services.access import (KvantObjectExistsMixin,
                                     KvantTeacherAndAdminAccessMixin)
from CoreApp.services.utils import ObjectManipulationManager
from django.urls import reverse_lazy as rl
from JournalApp.forms import KvantBaseSaveForm, KvantLessonSaveForm
from LoginApp.models import KvantUser
from openpyxl.utils import get_column_letter
from openpyxl.writer.excel import save_virtual_workbook
from RegisterApp.models import StaffPersonalInfo, StudentPersonalInfo
from RegisterApp.serializers import (StaffPersonalInfoSerializer,
                                     StudentPersonalInfoSerializer)

from .models import KvantCourse, KvantCourseType


class KvantAdminAccessMixin(KvantTeacherAndAdminAccessMixin):
    def _permissionTest(self, user):
        return user.permission == 'Администратор'


class KvantUserDeleteAccessMixin(KvantAdminAccessMixin, KvantObjectExistsMixin):
    request_object_arg = 'user_identifier'

    def _objectExiststTest(self, object_id):
        return KvantUser.objects.filter(id=object_id).exists()


class KvantCourseDeleteAccessMixin(KvantAdminAccessMixin, KvantObjectExistsMixin):
    request_object_arg = 'course_identifier'
    
    def _objectExiststTest(self, object_id):
        return KvantCourse.objects.filter(id=object_id).exists()


class KvantCourseTypeDeleteAccessMixin(KvantAdminAccessMixin, KvantObjectExistsMixin):
    request_object_arg = 'subject_identifier'

    def _objectExiststTest(self, object_id):
        return KvantCourseType.objects.filter(id=object_id).exists()


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
            return self._importUsersPersonalInfo(
                serializer=StudentPersonalInfoSerializer,
                users=StudentPersonalInfo.objects.filter(user__permission=user_type))
        return self._importUsersPersonalInfo(
            serializer=StaffPersonalInfoSerializer,
            users=StaffPersonalInfo.objects.filter(user__permission=user_type)
        )
    
    def _importUsersPersonalInfo(self, users, serializer):
        if not users.exists():
            return save_virtual_workbook(self._wb) 
        
        self._writeTable(self._parseTableHead(serializer(users.first()).data), 1)
        
        for i in range(len(users)):
            self._writeTable(self._parseTableData(serializer(users[i]).data), i + 2)
        return save_virtual_workbook(self._wb)

    def _writeTable(self, data, row):
        for col in range(len(data)):
            self._ws.cell(row=row, column=col + 1, value=data[col])
            self._ws.column_dimensions[get_column_letter(col + 1)].width = 30

    def _parseTableHead(self, data):
        table_head = []
        for col_name in data.keys():
            if isinstance(data[col_name], OrderedDict):
                generated_cols = self._parseTableHead(data[col_name])
                table_head += [f"{col_name} {sub_col_name}" for sub_col_name in generated_cols]
            else:
                table_head += [col_name]
        return table_head
    
    def _parseTableData(self, data):
        table_head = []
        for col_name in data.keys():
            if isinstance(data[col_name], OrderedDict):
                table_head += self._parseTableData(data[col_name])
            else:
                table_head += [data[col_name]]
        return table_head


class GenerateRegisterLink(ObjectManipulationManager):
    def __init__(self, forms, object=None):
        self._out_string = str()
        super(GenerateRegisterLink, self).__init__(forms, object)
    
    def createRegisterLink(self, request):
        links_or_errors = self._getCreatedObject(request)

        if not isinstance(links_or_errors, list):
            return '\n'.join([error.as_text() for error in links_or_errors.values()])
        
        for link_obj in links_or_errors:
            self._out_string += request.build_absolute_uri(f"{rl('register_page')}?key={link_obj.key}") + '\n'
        return self._out_string

    def _constructRedirectUrl(self, **kwargs): return


def getCourseById(course_id):
    """ Возвращает курс по его course_id """
    return KvantCourse.objects.get(id=course_id)


def getCourseTypeById(subject_id):
    return KvantCourseType.objects.get(id=subject_id)


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
