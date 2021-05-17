from . import views
from django.urls import path

urlpatterns = [
    path('<int:identifier>', views.diary_page, name='diary_page')
]
