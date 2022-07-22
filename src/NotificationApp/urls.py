from django.urls import path

from . import views

urlpatterns = [
    path('delete/', views.NotificationDeleteView.as_view(), name='delete_notification'),
]
