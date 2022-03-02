from . import views
from django.urls import path

urlpatterns = [
    path('box', views.MailListView.as_view(), name='mail_box'),
    path('create', views.MailCreationView.as_view(), name='create_mail'),
    path('delete/<int:mail_identifier>', views.MailDeleteView.as_view(), name='delete_mail'),
    path('detail/<int:mail_identifier>', views.MailDetailView.as_view(), name='mail_detail'),
    path('important/<int:mail_identifier>', views.MailChangeImportantStatusView.as_view(), name='make_important'),
]
