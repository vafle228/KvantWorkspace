from django.db import models
from LoginApp.models import KvantStudent, KvantTeacher
from DiaryApp.models import KvantLessonMark, KvantLessonHomeWork


class KvantCourse(models.Model):
    """
        Модель курса. Хранит в себе:
        имя курса (максимально 150 символов)
        учеников (связь с моделью KvantStudent из LoginApp) (связь ManyToMany)
        учитель (связь с моделью KvantTeacher из LoginApp) (связь ForeignKey)
    """
    name = models.CharField(max_length=150)
    students = models.ManyToManyField(KvantStudent, blank=True)
    teacher = models.ForeignKey(KvantTeacher, on_delete=models.CASCADE)

    def __str__(self):
        return f'Курс {self.name}'


class KvantLesson(models.Model):
    """
        Модель урока. Хранит в себе:
        дату урока (выставляется вручную, при генерации),
        время урока (выставляется вручную, при генерации),
        оценки за урок (связь с KvantLessonMark из DiaryApp) (связь ManyToMany)
        принадлежность к курсу (связь с KvantCourse из AdminModule) (связь ForeignKey)
        задание (связь с KvantLessonHomeWork из DiaryApp) (связь ManyToMany)
    """
    date = models.DateField()
    time = models.TimeField()
    mark = models.ManyToManyField(KvantLessonMark, blank=True)
    course = models.ForeignKey(KvantCourse, on_delete=models.CASCADE)
    task = models.ManyToManyField(KvantLessonHomeWork, blank=True)

    def __str__(self):
        return f'Урок {self.date}'
