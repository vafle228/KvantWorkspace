from . import views
from django.urls import path

urlpatterns = [
    path('<int:identifier>/box', views.MailPageTemplateView.as_view(), name='mail_box'),
    # path('<int:identifier>/create', views.create_mail, name='create_mail'),
    path('<int:identifier>/send', views.MailListView.as_view(), name='send_mails'),
    # path('<int:identifier>/read', views.change_read_status, name='change_status'),
    # path('<int:identifier>/important', views.change_important_status, name='change_important')
]
