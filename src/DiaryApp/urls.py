from django.urls import path

from . import views as ctr


urlpatterns = [
    path('', ctr.DiaryPageListView.as_view(), name='diary_page'),
    path('get/task/<int:task_identifier>', ctr.TaskDetailView.as_view(), name='task_detail'),
    path('get/lesson/<int:lesson_identifier>', ctr.LessonDetailView.as_view(), name='lesson_detail'),
]
