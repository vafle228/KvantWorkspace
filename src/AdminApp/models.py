from django.db import models


WEEK_DAYS = (
    ('Пн', 'Понедельник'),
    ('Вт', 'Вторник'),
    ('Ср', 'Среда'),
    ('Чт', 'Четверг'),
    ('Пт', 'Пятница'),
    ('Сб', 'Суббота'),
    ('Вс', 'Воскресенье'),
)


def getCoursePath(instance, filename):
    return f'courses/{instance.name}/{filename}'


class KvantCourseType(models.Model):
    name    = models.CharField(max_length=100, unique=True)
    image   = models.ImageField(blank=False, upload_to=getCoursePath)

    def __str__(self):
        return f'Тип курса: {self.name}'
    

    class Meta:
        db_table = 'course_type' 


class KvantCourseShedule(models.Model):
    week_day    = models.CharField(max_length=20, choices=WEEK_DAYS)
    time        = models.TimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return f'Рассписание на {self.week_day} в {self.time}'
    
    class Meta:
        db_table = 'course_shedule' 


class KvantCourse(models.Model):
    name        = models.CharField(max_length=20)
    schedule    = models.ManyToManyField(KvantCourseShedule, blank=False)
    type        = models.ForeignKey(KvantCourseType, on_delete=models.CASCADE)
    students    = models.ManyToManyField(to='LoginApp.KvantUser', blank=True, related_name="student")
    teacher     = models.ForeignKey(to='LoginApp.KvantUser', on_delete=models.CASCADE, related_name="teacher")

    def __str__(self):
        return f'{self.type.name} {self.name}'
    
    class Meta:
        db_table = 'kvant_course' 
