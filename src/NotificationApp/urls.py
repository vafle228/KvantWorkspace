from django.urls import path

from . import views

urlpatterns = [
    path('delete/<int:news_identifier>', views.NotificationDeleteView.as_view(), name='delete_notification'),
]
