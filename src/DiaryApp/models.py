from django.db import models
from django.utils import timezone


MARKS = (
    ('1', '1'), ('2', '2'),
    ('3', '3'), ('4', '4'),
    ('ОТ', 'ОТ'), ('УП', 'УП')
)


class KvantTaskMark(models.Model):
    mark    = models.CharField(max_length=10, choices=MARKS)
    student = models.ForeignKey(to='LoginApp.KvantUser', on_delete=models.CASCADE)

    class Meta:
        db_table = 'lesson_mark'

    def __str__(self):
        return f'Отметка {self.mark} {self.student}'


class KvantTaskBase(models.Model):
    description = models.TextField(null=False)
    title       = models.CharField(max_length=100)
    marks       = models.ManyToManyField(KvantTaskMark, blank=True)
    files       = models.ManyToManyField(to='CoreApp.FileStorage', blank=True)

    class Meta:
        db_table = 'lesson_base'

    def __str__(self):
        return f'Основа для {self.id}'
    


class KvantHomeWork(models.Model):
    text    = models.TextField(null=False)
    files   = models.ManyToManyField(to='CoreApp.FileStorage', blank=True)
    sender  = models.ForeignKey(to='LoginApp.KvantUser', on_delete=models.CASCADE)

    class Meta:
        db_table = 'task_work'

    def __str__(self):
        return f'Работа {self.sender}'


class KvantHomeTask(models.Model):
    works   = models.ManyToManyField(KvantHomeWork, blank=True)
    base    = models.OneToOneField(KvantTaskBase, on_delete=models.CASCADE)

    class Meta:
        db_table = 'kvant_task'

    def __str__(self):
        return f'Задание {self.id}'


class KvantLesson(models.Model):
    date    = models.DateField(default=timezone.now)
    tasks   = models.ManyToManyField(KvantHomeTask, blank=True)
    base    = models.OneToOneField(KvantTaskBase, on_delete=models.CASCADE)
    course  = models.ForeignKey(to='AdminApp.KvantCourse', on_delete=models.CASCADE, blank=False)    

    class Meta:
        db_table = 'kvant_lesson'

    def __str__(self):
        return f'Урок {self.base.title} на {self.date}'
