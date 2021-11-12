from django.db import models
from django.utils import timezone
from LoginApp.models import KvantUser
from AdminModule.models import KvantCourse
from SystemModule.models import FileStorage


MARKS = (
    ('1', '1'), ('2', '2'),
    ('3', '3'), ('4', '4'),
    ('ОТ', 'ОТ'), ('УП', 'УП')
)

class KvantHomeWork(models.Model):
    text    = models.TextField(null=False)
    mark    = models.CharField(max_length=10, choices=MARKS)
    files   = models.ManyToManyField(FileStorage, blank=True)
    sender  = models.ForeignKey(KvantUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'Работа {self.sender}'


class KvantHomeTask(models.Model):
    task    = models.TextField(null=False)
    files   = models.ManyToManyField(FileStorage, blank=True)
    works   = models.ManyToManyField(KvantHomeWork, blank=True)

    def __str__(self):
        return f'Задание №{self.id}'


class KvantLessonMark(models.Model):
    mark    = models.CharField(max_length=10, choices=MARKS)
    student = models.ForeignKey(KvantUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'Оценка {self.mark} {self.student}'


class KvantLesson(models.Model):
    description = models.TextField(null=False)
    title       = models.CharField(max_length=100)
    date        = models.DateField(default=timezone.now)        
    files       = models.ManyToManyField(FileStorage, blank=True)
    mark        = models.ManyToManyField(KvantLessonMark, blank=True)
    course      = models.ForeignKey(KvantCourse, on_delete=models.CASCADE, blank=False)
    task        = models.ForeignKey(KvantHomeTask, on_delete=models.SET(None), blank=True, null=True)

    def __str__(self):
        return f'Урок: {self.title}'
