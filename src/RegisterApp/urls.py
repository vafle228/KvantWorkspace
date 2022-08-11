from django.urls import path

from . import views

urlpatterns = [
    path('', views.RegisterPageTemplateView.as_view(), name='register_page'),
    path('user/create', views.UserCreateView.as_view(), name='register_user'),
]
