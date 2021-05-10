from . import views
from django.urls import path

urlpatterns = [
    path('<int:identifier>/box', views.mail_page, name='mail_box'),
    path('<int:identifier>/send', views.send_more_mails, name='send_mails'),
    path('<int:identifier>/update', views.change_mail_status, name='change_status'),
]