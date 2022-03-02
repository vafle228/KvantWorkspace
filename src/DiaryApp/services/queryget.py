from DiaryApp.models import KvantLesson


def getDiaryLessonQuery(user):
    """ Возвращает уроки ученика """
    return KvantLesson.objects.filter(course__students=user)
