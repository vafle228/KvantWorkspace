from django.db import models
from LoginApp.models import KvantStudent
from SystemModule.models import FileStorage

marks = (
    ('1', '1'), ('2', '2'),
    ('3', '3'), ('4', '4'),
    ('ОТ', 'ОТ'), ('УП', 'УП')
)


class KvantLessonHomeWork(models.Model):
    """
        Модель заданий ученика. Хранит в себе:
        текст задания (неограничано по символам),
        файлы (связь с моделью FileStorage из SystemModule)(связь ManyToMany),
        ученики (связь с моделью KvanStudent из LoginApp) (связь ManyToMany)

        !Модель ученика предполагает возможность добавить задание для определенных учеников
    """
    task = models.TextField()
    file = models.ManyToManyField(FileStorage, blank=True)
    students = models.ManyToManyField(KvantStudent, blank=True)

    def __str__(self):
        return f'Задание для: ' + ', '.join([student.student.__str__() for student in self.students.all()])


class KvantLessonMark(models.Model):
    """
        Модель оценок. Хранит в себе:
        оценку (от 1 до 4 или отсутвие по уважительной/нет причине)
        студента (связь с моделью KvantStudent из LoginApp) (сязь ForeignKey)
    """
    mark = models.CharField(max_length=150, choices=marks)
    student = models.ForeignKey(KvantStudent, on_delete=models.CASCADE)

    def __str__(self):
        return f'Оценка {self.mark}; {self.student}'
