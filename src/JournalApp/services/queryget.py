from DiaryApp.models import KvantLesson, KvantTaskBase


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
            '1': lambda course: KvantLesson.objects.filter(course=course, date__month__lte=6),
            '2': lambda course: KvantLesson.objects.filter(course=course, date__month__gte=7),
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
