from django.urls import path
from .views import change_user_theme

urlpatterns = [
    path('<int:identifier>', change_user_theme, name='change_theme')
]
