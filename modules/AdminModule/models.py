from django.db import models
from LoginApp.models import KvantUser


def get_course_path(instance, filename):
    return f'courses/{instance.name}/{filename}'


class KvantCourseType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(blank=False, upload_to=get_course_path)

    def __str__(self):
        return f'Тип курса: {self.name}'


class KvantCourse(models.Model):
    name        = models.CharField(max_length=20)
    type        = models.ForeignKey(KvantCourseType, on_delete=models.CASCADE)
    students    = models.ManyToManyField(KvantUser, blank=True, related_name="student")
    teacher     = models.ForeignKey(KvantUser, on_delete=models.CASCADE, related_name="teacher")

    def __str__(self):
        return f'Курс {self.type.name} {self.name}'
