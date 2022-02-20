from django.urls import path
from .views import ChangeUserCustomizationView


urlpatterns = [
    path('<int:identifier>/customization', ChangeUserCustomizationView.as_view(), name='change_theme'),
]