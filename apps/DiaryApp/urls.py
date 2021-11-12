from . import views
from django.urls import path

urlpatterns = [
    path('<int:identifier>', views.DiaryPageListView.as_view(), name='diary_page'),
    path('<int:identifier>/detail/<int:lesson_identifier>', views.DiaryLessonDetailView.as_view(), name='lesson_detail')
]
