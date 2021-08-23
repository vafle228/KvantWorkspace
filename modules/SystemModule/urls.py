from django.urls import path
from .views import UserLogOutView, UserThemeChangeView

urlpatterns = [
    path('<int:identifier>/logout', UserLogOutView.as_view(), name='logout_user'),
    path('<int:identifier>/theme', UserThemeChangeView.as_view(), name='change_theme'),
]
