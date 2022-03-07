from django.urls import path

from . import views as ctr


urlpatterns = [
    path('', ctr.DiaryPageListView.as_view(), name='diary_page'),
    path('create/work', ctr.HomeWorkCreateView.as_view(), name='create_work'),
    path('get/task/<int:task_identifier>', ctr.TaskDetailView.as_view(), name='task_detail'),
    path('update/work/<int:work_identifier>', ctr.HomeWorkUpdateView.as_view(), name='update_work'),
    path('get/lesson/<int:lesson_identifier>', ctr.LessonDetailView.as_view(), name='lesson_detail'),
]
