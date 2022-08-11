from django.urls import path

from . import views

urlpatterns = [
    path('', views.RegisterPageTemplateView.as_view(), name='register'),
]
