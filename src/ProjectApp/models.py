from django.db import models
from django.utils import timezone


PRIORITY = (
    ('low', 'Низкий'),
    ('high', 'Высокий'),
    ('medium', 'Средний'),
    ('none', 'Нет'),
)

TYPES = (
    ('Бэклог', 'Бэклог'),
    ('Задачи', 'Задачи'),
    ('В прогрессе', 'В прогрессе'),
    ('Выполнено', 'Выполнено'),
    ('Архив', 'Архив'),
)


class KvantProjectTask(models.Model):
    description     = models.TextField(blank=True)
    title           = models.CharField(max_length=255)
    deadline        = models.DateField(blank=True, null=True)
    participants    = models.ManyToManyField(to='LoginApp.KvantUser', blank=True)
    files           = models.ManyToManyField(to='CoreApp.FileStorage', blank=True)
    type            = models.CharField(max_length=100, choices=TYPES, default='Бэклог')
    priority        = models.CharField(max_length=100, choices=PRIORITY, default='none')

    class Meta:
        db_table = 'project_task'
    
    def __str__(self):
        return f'Задание {self.title} до {self.deadline}'


class KvantProjectMembershipRequest(models.Model):
    text    = models.TextField(blank=True)
    sender  = models.ForeignKey(to='LoginApp.KvantUser', on_delete=models.CASCADE)

    class Meta:
        db_table = 'member_request'
    
    def __str__(self):
        return f'Запрос на вступление от {self.sender}'


def setDefaultImage():
    from os.path import join
    from django.conf import settings
    from storages.backends.s3boto3 import S3Boto3Storage

    bucket = S3Boto3Storage()
    if not bucket.exists(settings.PROJECT_DEFAULT_IMAGE):
        with open(join(settings.MEDIA_ROOT + settings.PROJECT_DEFAULT_IMAGE), 'b+r') as f:
            bucket.save(settings.PROJECT_DEFAULT_IMAGE, f)
    return settings.PROJECT_DEFAULT_IMAGE


def getPath(instance, filename):
    return f'projects/img/{instance.date}/{instance.title}/{filename}'


class KvantProject(models.Model):
    description     = models.TextField()
    title           = models.CharField(max_length=255)
    date            = models.DateField(default=timezone.now)
    files           = models.ManyToManyField(to='CoreApp.FileStorage', blank=True)
    image           = models.ImageField(default=setDefaultImage, upload_to=getPath)
    course_subject  = models.ManyToManyField(to='AdminApp.KvantCourseType', blank=False)
    
    team            = models.ManyToManyField(to='LoginApp.KvantUser', blank=True, related_name='team')
    tutor           = models.ForeignKey(to='LoginApp.KvantUser', blank=False, on_delete=models.CASCADE, related_name='tutor')
    teamleader      = models.ForeignKey(to='LoginApp.KvantUser', blank=False, on_delete=models.CASCADE, related_name='teamleader')
    
    tasks           = models.ManyToManyField(KvantProjectTask, blank=True)

    class Meta:
        db_table = 'kvant_project'
        ordering = ['-date', '-id']
    
    def __str__(self):
        return f'Проект {self.title}'


class ActiveKvantProject(models.Model):
    chat        = models.ManyToManyField(to='ChatApp.ChatMessage', blank=True)
    project     = models.OneToOneField(KvantProject, on_delete=models.CASCADE)

    class Meta:
        db_table = 'active_project'
    
    def __str__(self):
        return f'Активный проект {self.project}'


class MemberHiringKvantProject(models.Model):
    requests    = models.ManyToManyField(KvantProjectMembershipRequest, blank=True)
    project     = models.OneToOneField(ActiveKvantProject, on_delete=models.CASCADE)

    class Meta:
        db_table = 'hiring_project'
    
    def __str__(self):
        return f'Проект {self.project} в поиске'


class ClosedKvantProject(models.Model):
    date    = models.DateField(default=timezone.now)
    project = models.OneToOneField(KvantProject, on_delete=models.CASCADE)

    class Meta:
        db_table = 'closed_project'
    
    def __str__(self):
        return f'Закрытый проект {self.project}'
