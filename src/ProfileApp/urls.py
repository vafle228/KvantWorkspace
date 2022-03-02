from . import views
from django.urls import path

urlpatterns = [
    path('<int:identifier>/box', views.MailListView.as_view(), name='mail_box'),
    path('<int:identifier>/create', views.MailCreationView.as_view(), name='create_mail'),
    path('<int:identifier>/delete/<int:mail_identifier>', views.MailDeleteView.as_view(), name='delete_mail'),
    path('<int:identifier>/detail/<int:mail_identifier>', views.MailDetailView.as_view(), name='mail_detail'),
    path('<int:identifier>/important/<int:mail_identifier>', views.MailChangeImportantStatusView.as_view(), name='make_important'),
]
