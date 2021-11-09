from . import views
from django.urls import path

urlpatterns = [
    path('<int:identifier>', views.DiaryPageListView.as_view(), name='diary_page')
]
