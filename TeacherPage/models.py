from django.db import models
from LoginPage.models import KvantUser
from StudentPage.models import FileStorage

marks = (
    ('1', '1'), ('2', '2'),
    ('3', '3'), ('4', '4'),
    ('ОТ', 'ОТ'), ('УП', 'УП')
)


class KvantLessonHomeWork(models.Model):
    task = models.TextField()
    file = models.ManyToManyField(FileStorage)

    def __str__(self):
        return f'Задание на {str(self.kvantlesson)}'


class KvantLessonMark(models.Model):
    mark = models.CharField(max_length=150, choices=marks)
    student = models.ForeignKey(KvantUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'Оценка {self.mark}; {self.student}'
