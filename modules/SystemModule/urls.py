from . import views
from django.urls import path

urlpatterns = [
    path('<int:identifier>/logout', views.logout_user, name='logout_user'),
    path('<int:identifier>/theme', views.change_user_theme, name='change_theme'),
]
