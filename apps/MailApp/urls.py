from . import views
from django.urls import path

urlpatterns = [
    path('<int:identifier>/box', views.MailListView.as_view(), name='mail_box'),
    path('<int:identifier>/create', views.MailCreationView.as_view(), name='create_mail'),
    path('<int:identifier>/important', views.MailChangeImportantStatusView.as_view(), name='make_important'),
    path('<int:identifier>/detail/<int:mail_identifier>', views.MailDetailView.as_view(), name='mail_detail'),
]
