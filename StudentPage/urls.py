from . import views
from django.urls import path

urlpatterns = [
    path('<int:identifier>', views.main_page, name='student_page'),
    path('<int:identifier>/diary/', views.dairy_page, name='student_diary'),
    path('<int:identifier>/mail/', views.mail_page, name='student_mail'),
    path('<int:identifier>/statistics/', views.statistics_page, name='student_statistics'),
]
