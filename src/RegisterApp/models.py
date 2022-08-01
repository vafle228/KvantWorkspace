# from django.db import models


# class KvantUserParantContactInfo(models.Model):
#     work_place      = models.TextField()
#     work_position   = models.TextField()
#     birth_date      = models.DateField(blank=True)
#     email           = models.EmailField(blank=True)
#     phone_number    = models.CharField(max_length=50)
#     name            = models.CharField(max_length=100)
#     surname         = models.CharField(max_length=100)
#     patronymic      = models.CharField(max_length=100, blank=True)


# class KvantUserContactInfo(models.Model):
#     user = models.OneToOneField(to="LoginApp.KvantUser", on_delete=models.CASCADE)
    
#     mother = models.OneToOneField(
#         KvantUserParantContactInfo, related_name='mother',
#         on_delete=models.SET_NULL, null=True, blank=True)
    
#     father = models.OneToOneField(
#         KvantUserParantContactInfo, related_name='father',
#         on_delete=models.SET_NULL, null=True, blank=True)
    
#     birth_date = models.DateField(blank=True)
#     SNILS = models.CharField(max_length=255)
#     phone_number = models.CharField(max_length=50)
#     home_address = models.CharField(max_length=255)

#     school = models.CharField(max_length=255)
#     grade = models.CharField(max_length=255)
