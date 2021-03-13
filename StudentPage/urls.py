from . import views
from django.urls import path

urlpatterns = [
    path('', views.main_page, name='student_page'),
    path('diary/', views.dairy_page, name='student_diary'),
    path('mail/', views.mail_page, name='student_mail'),
    path('statistics/', views.statistics_page, name='student_statistics')
]
