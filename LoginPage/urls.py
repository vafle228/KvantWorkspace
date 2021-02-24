from . import views
from django.urls import path

urlpatterns = [
    path('', views.login_page),
    path('login/', views.login_user, name='login'),
]