from . import views
from django.urls import path

urlpatterns = [
    path('<int:identifier>/box', views.MailListView.as_view(), name='mail_box'),
    path('<int:identifier>/create', views.MailCreationView.as_view(), name='create_mail'),
    path('<int:identifier>/detail/<int:mail_identifier>', views.MailDetailView.as_view(), name='mail_detail')
    # path('<int:identifier>/read', views.change_read_status, name='change_status'),
    # path('<int:identifier>/important', views.change_important_status, name='change_important')
]
