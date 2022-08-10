from django.db import models
from .validators import *


sexes = (
    ('Мужской', 'Мужской'),
    ('Женский', 'Женский'),
)


commit = (
    ('Да', 'Да'),
    ('Нет', 'Нет'),
)


class PersonalityDocument(models.Model):
    series      = models.CharField(max_length=255, blank=True)
    number      = models.CharField(max_length=255, blank=True)
    who_gave    = models.CharField(max_length=255, blank=True)
    code        = models.CharField(max_length=255, blank=True)
    given_date  = models.CharField(max_length=255, blank=True, validators=[validate_date])


class LivingAdress(models.Model):
    city            = models.CharField(max_length=255, blank=True)
    street          = models.CharField(max_length=255, blank=True)
    house_number    = models.CharField(max_length=255, blank=True)
    room            = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.city} {self.street} {self.house_number} {self.room}'


class StudyDocument(models.Model):
    vpo_spo         = models.CharField(max_length=255, blank=True)
    vuz             = models.CharField(max_length=255, blank=True)
    speciality      = models.CharField(max_length=255, blank=True)
    qualification   = models.CharField(max_length=255, blank=True)
    year            = models.CharField(max_length=255, blank=True)


class StudentParent(models.Model):
    email       = models.EmailField(blank=True)
    name        = models.CharField(max_length=255, blank=True)
    surname     = models.CharField(max_length=255, blank=True)
    work_place  = models.CharField(max_length=255, blank=True)
    work_title  = models.CharField(max_length=255, blank=True)
    patronymic  = models.CharField(max_length=255, blank=True)
    date        = models.CharField(max_length=255, blank=True, validators=[validate_date])
    telephone   = models.CharField(max_length=255, validators=[validate_telephone], blank=True)
    adress      = models.OneToOneField(LivingAdress, on_delete=models.SET_NULL, null=True, blank=True)
    document    = models.OneToOneField(PersonalityDocument, on_delete=models.SET_NULL, null=True, blank=True)


class StudentPersonalInfo(models.Model):
    user            = models.OneToOneField(to='LoginApp.KvantUser', on_delete=models.CASCADE)
    
    school          = models.CharField(max_length=255, blank=True)
    school_class    = models.CharField(max_length=255, blank=True)
    sex             = models.CharField(max_length=255, choices=sexes, blank=True)
    is_dzd          = models.CharField(max_length=255, choices=commit, blank=True)
    date            = models.CharField(max_length=255, blank=True, validators=[validate_date])
    snils           = models.CharField(max_length=255, validators=[validate_snils], blank=True)
    telephone       = models.CharField(max_length=255, validators=[validate_telephone], blank=True)
    adress          = models.OneToOneField(LivingAdress, on_delete=models.SET_NULL, null=True, blank=True)
    document        = models.OneToOneField(PersonalityDocument, on_delete=models.SET_NULL, null=True, blank=True)

    mother          = models.OneToOneField(StudentParent, on_delete=models.SET_NULL, null=True, blank=True, related_name='mother')
    father          = models.OneToOneField(StudentParent, on_delete=models.SET_NULL, null=True, blank=True, related_name='father')


class StaffPersonalInfo(models.Model):
    user            = models.OneToOneField(to='LoginApp.KvantUser', on_delete=models.CASCADE, blank=True)

    sex             = models.CharField(max_length=255, choices=sexes, blank=True)
    date            = models.CharField(max_length=255, blank=True, validators=[validate_date])
    snils           = models.CharField(max_length=255, validators=[validate_snils], blank=True)
    telephone       = models.CharField(max_length=255, validators=[validate_telephone], blank=True)
    adress          = models.OneToOneField(LivingAdress, on_delete=models.SET_NULL, null=True, blank=True)
    study           = models.OneToOneField(StudyDocument, on_delete=models.SET_NULL, null=True, blank=True)
    document        = models.OneToOneField(PersonalityDocument, on_delete=models.SET_NULL, null=True, blank=True)
