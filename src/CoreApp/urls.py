from django.urls import path
from .views import ChangeUserCustomizationView


urlpatterns = [
    path('customization', ChangeUserCustomizationView.as_view(), name='change_theme'),
]