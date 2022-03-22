from django.urls import path

from . import views

urlpatterns = [
    path('catalog/', views.ProjectCatalogTemplateView.as_view(), name='project_catalog'),
    path('task/<int:task_identifier>', views.ProjectTaskDetailView.as_view(), name='task_view'),
    path('info/<int:project_identifier>', views.ProjectInfoDetailView.as_view(), name='project_info'),
    path('task/update/<int:task_identifier>', views.ProjectTaskUpdateView.as_view(), name='update_task'),
    path('tasks/<int:project_identifier>', views.ProjectWorkspaceDetailView.as_view(), name='project_tasks'),
]
